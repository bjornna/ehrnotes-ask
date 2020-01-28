import xml.dom.minidom
ns = {"d5p1": "http://www.welldiagnostics.com/spp"}


def main():
    doc = xml.dom.minidom.parse("spp/hst_spp.xml")
    services = doc.getElementsByTagName("MedicalService")
    n = 1
    counter = 0
    for s in services:
        counter += 1
        print("Service")
        ids = s.getElementsByTagName("Id")

        for id in ids:
            #print(id.getAttribute("Type", namespaces=ns))
            print(id.attributes.items())
            # print(id.attributes.items()[1][1])
        if counter > n:
            break


if __name__ == "__main__":
    main()
