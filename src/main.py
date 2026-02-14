from scrapper.scrap import OuterHtml
from scrapper.config.paths import PathConfig

def main():
    scrap_outer_html = OuterHtml()
    file_path = PathConfig()

    scrap_outer_html.scrap_outer_html(file_path)

if __name__ == "__main__":
    main()