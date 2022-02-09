import threading
import sys
import pickle
import tkinter as tk
import signal

NUM_PIXELS = 8
WINDOW_HEIGHT_PX = 80
WINDOW_WIDTH_PX = WINDOW_HEIGHT_PX * NUM_PIXELS

PIXEL_WIDTH = WINDOW_WIDTH_PX / NUM_PIXELS

DRAW_TIMEOUT_MS = 100


class TkPhatSimulator():
    def __init__(self):
        self.brightness = 70
        self.do_run = True
        self.data = [[0, 0, 0, 7] for _ in range(8)]

        self.root = tk.Tk()
        self.root.resizable(False, False)

        self.root.bind('<Control-c>', lambda _: self.destroy())
        self.root.bind("<Unmap>", lambda _: self.destroy())
        self.root.protocol('WM_DELETE_WINDOW', self.destroy)

        self.root.title('Blinkt! simulator')
        self.root.geometry('{}x{}'.format(WINDOW_WIDTH_PX, WINDOW_HEIGHT_PX))
        self.canvas = tk.Canvas(
            self.root, width=WINDOW_WIDTH_PX, height=WINDOW_HEIGHT_PX)
        self.canvas.config(highlightthickness=0)

    def run(self):
        try:
            self.draw_pixels()
            self.root.mainloop()
        except Exception as e:
            self.destroy()
            raise e

    def destroy(self):
        self.do_run = False

    def running(self):
        return self.do_run

    def draw_pixels(self):
        if not self.running():
            self.root.destroy()
            return

        self.canvas.delete(tk.ALL)
        self.canvas.create_rectangle(
            0, 0,
            WINDOW_WIDTH_PX, WINDOW_HEIGHT_PX, width=0, fill='black')

        for x in range(NUM_PIXELS):
            pixel = self.data[x]
            color = '#{0:02x}{1:02x}{2:02x}'.format(*pixel)
            self.canvas.create_rectangle(
                x * WINDOW_HEIGHT_PX, 0,
                x * WINDOW_HEIGHT_PX + WINDOW_HEIGHT_PX,
                WINDOW_HEIGHT_PX,
                width=0, fill=color)

        self.canvas.pack()

        self.root.after(DRAW_TIMEOUT_MS, self.draw_pixels)

    def set_data(self, data):
        self.data = data


class ReadThread:
    def __init__(self, simulator):
        self.simulator = simulator
        self.stdin_thread = threading.Thread(
            target=self._read_stdin, daemon=True)

    def start(self):
        self.stdin_thread.start()

    def join(self):
        self.stdin_thread.join()

    def _read_stdin(self):
        while self.simulator.running():
            try:
                self._handle_update(pickle.load(sys.stdin.buffer))
            except EOFError:
                self.simulator.destroy()
            except Exception as err:
                self.simulator.destroy()
                raise err

    def _handle_update(self, buffer):
        self.simulator.set_data(buffer)


def main():
    print('Blinkt! simulator')

    signal.signal(signal.SIGINT, lambda sig, frame: sys.exit(0))

    phat = TkPhatSimulator()
    thread = ReadThread(phat)
    thread.start()
    phat.run()
    thread.join()


if __name__ == "__main__":
    main()
