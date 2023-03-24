

if __name__ == "__main__":
    rows = 40
    cols = 40
    num = rows * cols

    app = QApplication(sys.argv)
    main_window = MainWindow(rows, cols)
    eratosthenes = Eratosthenes(num, main_window)
    async_helper = AsyncHelper(entry=eratosthenes.start)

    # This establishes the entry point for the Trio guest run. It varies
    # depending on how and when its event loop is to be triggered, e.g.,
    # from the beginning (as here) or rather at a specific moment like
    # a button press.
    QTimer.singleShot(0, async_helper.launch_guest_run)

    main_window.show()

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app.exec()
