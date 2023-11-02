from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field, asdict
from time import time

import pandas as pd
from dacite import from_dict

import gandai as ts
from gandai import query, models, gpt
from gandai.sources import GrataWrapper as grata
from gandai.sources import GoogleMapsWrapper as google

import requests
from bs4 import BeautifulSoup
import json


@dataclass
class Review:
    was_acquired: str  # Is there any news indicating that this company has already been acquired? Start your answer with one of ['Yes,','No,']
    products: str = field(default="")  # csv of the products offered by the company
    services: str = field(default="")  # csv of the services offered by the company
    customers: str = field(default="")  # csv of the customers of the company


def enrich_with_gpt(domain: str) -> None:
    company = ts.query.find_company_by_domain(domain)
    print(domain)
    q = f"{company.name}  acquired"
    page_one = ts.google.page_one(q)[["title", "link", "snippet"]]
    page_one = page_one.to_dict(orient="records")

    resp = requests.get(f"http://www.{domain}")
    soup = BeautifulSoup(resp.text, "html.parser")
    homepage_text = soup.text.strip()

    review = """
    @dataclass
    class Review:
        was_acquired: str # Is there any news indicating that this company has already been acquired? Start your answer with one of ['Yes,','No,']
        products: str = field(default="") # csv of the products offered by the company. products are physical goods sold by the company. do not list services here.
        services: str = field(default="") # csv of the services offered by the company. services are intangible goods sold by the company. do not list products here.
        customer: str = field(default="") # csv of the customers of the company. customers are the people or companies that buy the products or services. do not list suppliers here.
    """

    messages = [
        {
            "role": "system",
            "content": f"You are a helpful assistant evaulating {company.name} for acquisition.",
        },
        {
            "role": "system",
            "content": f"Companies that have already been acquired by private equity are not a good fit.",
        },
        {
            "role": "system",
            "content": f"Here are the google results for '{q}': {page_one}",
        },
        {"role": "system", "content": f"Here is the homepage_text {homepage_text}"},
        {
            "role": "system",
            "content": f"if the homepage_text indicates the web scraping failed or was blocked, ignore the homepage_text and return 'unknown' for products, services, and customers",
        },
        {
            "role": "user",
            "content": f"You are to create a Review {review}, fill it out and return it to me as JSON. Respond with only the json object.",
        },
    ]

    resp = ts.gpt.ask_gpt35(messages)
    review = from_dict(data_class=Review, data=json.loads(resp))
    print(review)
    company.meta = {**company.meta, **asdict(review)}
    ts.query.update_company(company)


def enrich_with_grata(company: str) -> None:
    resp = grata.enrich(company.domain)
    company.name = company.name or resp.get("name")
    company.description = resp.get("description")
    company.meta = {**company.meta, **resp}
    query.update_company(company)


def enrich_company(domain: str) -> None:
    company = query.find_company_by_domain(domain)
    if "company_uid" not in company.meta.keys():
        enrich_with_grata(company)
    if "was_acquired" not in company.meta.keys():
        enrich_with_gpt(domain)


def run_similarity_search(search: models.Search, domain: str) -> None:
    # dealcloud_companies =
    grata_companies = grata.find_similar(domain=domain, search=search)
    query.insert_companies_as_targets(
        companies=grata_companies, search_uid=search.uid, actor_key="grata"
    )


def run_criteria_search(search: models.Search) -> None:
    # don't have to pass the event because the criteria
    # is the event that we're responding to
    grata_companies = grata.find_by_criteria(search)
    query.insert_companies_as_targets(
        companies=grata_companies, search_uid=search.uid, actor_key="grata"
    )


def run_maps_search(search: models.Search, event: models.Event) -> None:
    print("running maps search... may take 30++ seconds")
    start = time()
    top_n = event.data.get("top_n", 1)
    radius_miles = event.data.get("radius", 10)

    def process_area(area: str) -> None:
        centroids = gpt.get_top_zip_codes(area=area, top_n=top_n)
        print(f"searching {area} with {len(centroids)} centroids: {centroids}")

        place_ids = google.fetch_unique_place_ids(
            search_phrase=event.data["phrase"],
            locations=centroids,
            radius_miles=radius_miles,
        )
        print(f"{len(place_ids)} place_ids found in {area}")

        with ThreadPoolExecutor(max_workers=10) as executor:
            for place_id in place_ids:
                executor.submit(
                    google.build_target_from_place_id,
                    place_id=place_id,
                    search_uid=search.uid,
                    append_to_prompt=event.data["prompt"],
                )

    # with ThreadPoolExecutor(max_workers=5) as executor:
    #     executor.map(process_area, e.data["areas"])
    for area in event.data["areas"]:
        process_area(area)

    print(f"🗺  Maps took {time() - start} seconds")


def process_event(event_id: int) -> None:
    print("processing event...")

    event: models.Event = query.find_event_by_id(event_id)
    print(event)
    search = query.find_search(
        uid=event.search_uid
    )  # this would fail if insert search is an event
    domain = event.domain
    if event.type == "create":
        enrich_company(domain=domain)  # lets unleash the beast
        # gpt enrich here
        # pass
    elif event.type == "advance":
        enrich_company(domain=domain)
    elif event.type == "validate":
        enrich_company(domain=domain)
        run_similarity_search(search=search, domain=domain)

    elif event.type == "send":
        enrich_company(domain=domain)
    elif event.type == "client_approve":
        enrich_company(domain=domain)
        run_similarity_search(search=search, domain=domain)  # n=
    elif event.type == "reject":
        pass
    elif event.type == "client_reject":
        pass
    elif event.type == "conflict":
        enrich_company(domain=domain)
        run_similarity_search(search=search, domain=domain)
    elif event.type == "client_conflict":
        enrich_company(domain=domain)
        run_similarity_search(search=search, domain=domain)
    elif event.type == "criteria":
        if len(event.data["inclusion"]["keywords"]) > 0:
            run_criteria_search(search=search)

    elif event.type == "maps":
        run_maps_search(search=search, event=event)

    elif event.type == "google":
        q = event.data["q"]
        results = ts.google.page_one(q)[["title", "link", "snippet"]]
        results["domain"] = results["link"].apply(lambda x: ts.helpers.clean_domain(x))
        results = results.rename(columns={"snippet": "description"})
        print(results)
        ts.query.insert_companies_as_targets(
            companies=results[["domain", "description"]].to_dict(orient="records"),
            search_uid=event.search_uid,
            actor_key=event.actor_key,
        )

    elif event.type == "import":
        data = event.data
        query.insert_targets_from_domains(
            domains=data["domains"],
            search_uid=event.search_uid,
            actor_key=event.actor_key,
            stage=data.get("stage", "advance"),
        )

    elif event.type == "reset":
        print("💣 Resetting Inbox...")
        query.reset_inbox(search_uid=search.uid)

    elif event.type == "update":
        if domain:
            company = query.find_company_by_domain(domain)
            if event.data.get("name"):
                company.name = event.data["name"]
            if event.data.get("description"):
                description = event.data["description"]
                if description.startswith("/gpt"):
                    company.description = gpt.get_company_summary(domain=domain)
                else:
                    company.description = event.data["description"]

            company.meta = {**company.meta, **event.data}
            query.update_company(company)
        else:
            search.meta = {**search.meta, **event.data}
            query.update_search(search)

    elif event.type == "transition":
        for domain in event.data["domains"]:
            query.insert_event(
                ts.models.Event(
                    search_uid=search.uid,
                    domain=domain,
                    type=event.data["type"],
                    actor_key=event.actor_key,
                )
            )
