import pandas as pd
import csv


def format_csv(data: pd.DataFrame) -> pd.DataFrame:
    # Create a new empty dataframe with one column "Text"
    new_data = data.dropna(subset=["source_glosa", "delito", "lugar", "comuna", "text"])
    new_data.sort_values(by="fecha", inplace=True)
    text_df = pd.DataFrame(columns=["Text"])
    text_df["Text"] = new_data.apply(lambda x: f"{x['fecha']} {x['source_glosa']} {x['delito']} {x['lugar']} {x['comuna']} {x['text']}", axis=1)
    text_df["Text"] = text_df["Text"].str.replace("\n", " ")

    return text_df

def csv2txt(data: pd.DataFrame, output_file: str) -> None:
    month_dict = { 
                    "01": "Enero",
                    "02": "Febrero",
                    "03": "Marzo",
                    "04": "Abril",
                    "05": "Mayo",
                    "06": "Junio",
                    "07": "Julio",
                    "08": "Agosto",
                    "09": "Septiembre",
                    "10": "Octubre",
                    "11": "Noviembre",
                    "12": "Diciembre"
                  }
    previous_month = ""
    with open(output_file, "w") as f:
        for text in data["Text"]:
            month = text.split(" ")[0].split("-")[1]
            year = text.split(" ")[0].split("-")[0]
            if month != previous_month:
                f.write(f"\n{month_dict[month]} {year}\n")
                previous_month = month
            f.write(f"{text}\n")


original_data = pd.read_csv("data/delitos_txt.csv")

formatted_data = format_csv(original_data)

formatted_data.to_csv("data/formatted_text.csv", index=False, quoting=csv.QUOTE_ALL)

csv2txt(formatted_data, "data/formatted_text.txt")