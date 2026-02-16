from scrapper.scrap import OuterHtml
from scrapper.parse_html import ParseData
from scrapper.config.paths import PathConfig

def main():
    # scrap_outer_html = OuterHtml()
    # file_path = PathConfig()

    # scrap_outer_html.scrap_outer_html(file_path)

    p = PathConfig()
    f = p.html_files
    a = ParseData(f)
    a.parse_data_to_list()


if __name__ == "__main__":
    main()