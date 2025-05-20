from scraping import scrap_data_to_excel
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrap data from otomoto.pl")
    parser.add_argument("-n", "--num-pages", type=int, default=1, help="Liczba stron do pobrania")
    parser.add_argument("-s", "--start-page", type=int, default=1, help="Numer strony początkowej")
    parser.add_argument("-o", "--output-filename", type=str, default="otomoto_data.xlsx", help="Nazwa pliku wyjściowego")
    args = parser.parse_args()

    if args.num_pages < 1:
        print("❌ Liczba stron musi być większa niż 0")
        exit(1)

    if args.start_page < 1:
        print("❌ Numer strony początkowej musi być większy niż 0")
        exit(1)

    if not args.output_filename.endswith(".xlsx"):
        print("❌ Nazwa pliku wyjściowego musi kończyć się na .xlsx")
        exit(1)

    scrap_data_to_excel(num_pages=args.num_pages, start_page=args.start_page, output_filename=args.output_filename)