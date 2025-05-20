from scraping import scrap_data_to_excel
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrap data from otomoto.pl")
    parser.add_argument("-n", "--num-pages", type=int, default=1, help="Liczba stron do pobrania")
    args = parser.parse_args()
    scrap_data_to_excel(num_pages=args.num_pages)