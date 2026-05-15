from app import App, ContentFrame


def main():
    app = App()
    frame = ContentFrame(app)
    app.mainloop()

if __name__ == "__main__":
    main()
