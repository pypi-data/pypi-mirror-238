from .imports import *
from . import _utils


def lektier(self):
    url = f"https://www.lectio.dk/lectio/{self.skoleId}/material_lektieoversigt.aspx?elevid={self.elevId}"
    resp = self.session.get(url)
    if resp.url != url:
        raise Exception("lectio-cookie udløbet")

    soup = BeautifulSoup(resp.text, "html.parser")

    lektier = []

    _dato = (
        soup.find("span", {"id": "s_m_masterfooternowSpan"})
        .text.split("  ")[0]
        .replace("-", "/")
        .split("/")
    )
    for tr in soup.find_all("tr")[1:]:
        lektie = {
            "dato": "",
            "aktivitet": {},
            "lektier": ""
        }
        for i, td in enumerate(tr.find_all("td")[:3]):
            if i == 0:
                dato = td.text.split(" ")[1]
                dato += (
                    f"-{int(_dato[2]) + 1}"
                    if dato.split("/")[1] == "1" and _dato[1] != "1"
                    else f"-{int(_dato[2])}"
                )
                lektie["dato"] = dato
            elif i == 1:
                modul = td.find("a", class_="s2skemabrik")
                modulDict = _utils.skemaBrikExtract(dato, modul)
                lektie["aktivitet"] = modulDict
            else:
                for element in str(td).replace("\xa0", "\n").replace("<br/>", "\n").replace("</a>", "</a>\n").split("\n"):
                    print(element)
                    elementSoup = BeautifulSoup(element, "html.parser")
                    if elementSoup.text != "":
                        if (elementWithHref := elementSoup.find("a", href=True)) != None:
                            href = elementWithHref.get("href")
                            if href.startswith(f"/lectio/{self.skoleId}"):
                                href = f"https://www.lectio.dk{href}"
                            lektie["lektier"] += unicodedata.normalize(
                                "NFKD", f"[{elementSoup.text.rstrip().lstrip()}]({href})\n"
                            )
                        else:
                            lektie["lektier"] += unicodedata.normalize(
                                "NFKD",
                                elementSoup.text.rstrip().lstrip().replace("\xa0", " ")
                                + "\n",
                            )

        lektier.append(lektie)

    return lektier
