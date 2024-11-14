import streamlit as st
from utils.receipt_processor import process_receipt
from utils.receipt_preprocess import preprocess_receipt

def main():
    st.title("Aplikacja do analizy paragonów")
    st.write("Wgraj plik JSON z paragonem, a aplikacja sprawdzi produkty w bazie Open Food Facts.")

    uploaded_file = st.file_uploader("Wybierz plik JSON z paragonem", type=["json"])

    if uploaded_file is not None:
        preprocesed_data = preprocess_receipt(uploaded_file)
        receipt_data = process_receipt(preprocesed_data)

        if receipt_data:
            for result in receipt_data:
                st.write(result)
        else:
            st.write("Brak wyników do wyświetlenia.")


if __name__ == "__main__":
    main()