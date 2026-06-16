from app import App, UserInterface


def main():
    app = App()
    app.resizable(False, False)
    frame = UserInterface(app)
    app.mainloop()

if __name__ == "__main__":
    main()
