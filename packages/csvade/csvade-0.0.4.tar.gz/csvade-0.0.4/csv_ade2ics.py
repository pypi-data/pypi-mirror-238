import datetime, csv, click
from urllib.parse import urlparse
from xml.etree.ElementTree import Element
from ics import Calendar, Event, Attendee
from pyade import ADEWebAPI, Config
from InquirerPy.inquirer import select as prompt_select


create_datetime = lambda date, hour: datetime.datetime.strptime(f"{date} {hour}", "%d/%m/%Y %H:%M")


class BetterADEWebAPI(ADEWebAPI):
    ...

    @staticmethod
    def get_event_additional_info(event: Element, info_key: str) -> str:
        """Get additional information from an event.

        Args:
            event (Element): the XML element corresponding to the event.
            info_key (str): the key (XML resource element->category) to search.

        Returns:
            str: the information data or an empty string.
        """
        infos = event.findall(f"resources/resource[@category='{info_key}']")
        if len(infos) > 0:
            return infos[0].get("name")
        return ""

    def getEvents(self, **kwargs) -> list[dict[str, str]]:
        function, typ = "getEvents", "event"
        self._test_opt_params(kwargs, function)
        element = self._send_request(function, **kwargs)
        events = element.findall(typ)
        result = []

        for event in events:
            classroom = self.get_event_additional_info(event, "classroom")
            instructor = self.get_event_additional_info(event, "instructor")
            result.append(event.attrib | {"classroom": classroom, "instructor": instructor})

        return result


@click.command()
@click.argument("csv_file", type=click.Path(exists=True), required=1)
@click.option("--url", "-u", help="The URL of the ADE API.")
@click.option("--login", "-l", help="The username used to connect to ADE.", default="")
@click.option("--password", "-p", help="The password used to connect to ADE.", default="")
@click.option("--out", "-o", type=click.Path(exists=False), help="The output file to generate.", default="caladar.ics")
def process_csv(csv_file: str, url: str, login: str, password: str, out: str):
    uri = urlparse(url)
    if not uri.scheme:
        url = "https://" + url
        uri = urlparse(url)

    if not url.endswith("/jsp/webapi"):
        url = f"{uri.scheme}://{uri.netloc}/jsp/webapi"
    if not out.endswith(".ics"):
        out += ".ics"
    # fmt:off
    calendar    = Calendar()
    config      = Config.create(url=url, login=login, password=password)
    ade         = BetterADEWebAPI(**config)
    # fmt:on
    assert ade.connect(), "Connection failed."

    project_id = prompt_select(
        message="Select an ADE project.",
        choices=[{"name": project["name"], "value": project["id"]} for project in ade.getProjects(detail=4)],
    ).execute()

    ade.setProject(project_id)

    with open(csv_file, "r") as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # skip first line (column names).

        for row in csv_reader:
            groups = row[0].split("_")
            if len(groups) < 5:
                continue
            resources = [
                resource["id"]
                for resource in ade.getResources(name=f"{groups[2]}-{groups[3]}", detail=4)
                if resource["isGroup"] == "true"
            ]

            for event in ade.getEvents(resources=resources, detail=8):
                calendar.events.add(
                    Event(
                        name=event["name"],
                        begin=create_datetime(event["date"], event["startHour"]),
                        end=create_datetime(event["date"], event["endHour"]),
                        location=event["classroom"],
                        attendees=[Attendee(email="", common_name=event["instructor"])],
                        description=event["instructor"],
                    )
                )

    with open(out, "w") as f:
        f.writelines(calendar.serialize_iter())
    click.echo(out)


if __name__ == "__main__":
    process_csv()
