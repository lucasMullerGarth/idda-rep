from aplicacao import Aplicacao

if __name__ == "__main__":
    app = Aplicacao()
    app.mainloop()
    try:
        import selenium
    except ImportError:
        print("A biblioteca 'selenium' não está instalada. Rode: pip install -r requirements.txt")
        exit()
        
   