# import modules
from PIL import ImageGrab, ImageOps # PIL to take screenshot
import pyautogui # to send commands to pc
import numpy as np # to process image
import matplotlib.pyplot as plt # to show images if it would be necessairy
import time # to use sleep

# create class Bot
class Bot:

    # initial values
    init_values = {
        'time_jump': 0.24,
        'wait': 0.038,
        'coord_jump': [140, 45, 185, 150],
        'coord_gameover': [90, 100, 180, 420],
        'coord_game': (180, 150, 850, 370),
        'image': np.zeros((500, 500))
    }

    def __init__(self):
        self.time_jump = self.init_values['time_jump']
        self.wait = self.init_values['wait']
        self.coord_jump = self.init_values['coord_jump'].copy()
        self.coord_gameover = self.init_values['coord_gameover'].copy()
        self.coord_game = self.init_values['coord_game']
        self.image = np.zeros((500, 500))


    def image_grab(self):
        image = ImageGrab.grab(self.coord_game)
        image = np.asarray(ImageOps.grayscale(image))
        self.image = image.copy()
        unique, counts = np.unique(image, return_counts = True)
        index_max = np.argmax(counts)
        max_value = unique[index_max]
        # print(max_value)
        if max_value > 33:
            self.image[image == max_value] = 33
            self.image[image == 0] = 33
            self.image[image > 200] = 0
        # plt.imshow(image_resp)


    def press_space(self):
        pyautogui.keyDown('space')
        time.sleep(self.time_jump)
        pyautogui.keyUp('space')

        time.sleep(self.wait)
        pyautogui.keyDown('down')
        pyautogui.keyUp('down')


    def restart_game(self):
        game_over_img = self.image[self.coord_gameover[0]:self.coord_gameover[1], self.coord_gameover[2]:self.coord_gameover[3]]
        game_over = game_over_img.copy()
        game_over[game_over < 150] = 0
        game_over[game_over >= 150] = 1
        not_zero = np.count_nonzero(np.sum(game_over, axis = 0))

        game_over_button_box = self.image[130:155, 280:320]
        game_over_button = game_over_button_box.copy()
        game_over_button[game_over_button_box < 150] = 0
        game_over_button[game_over_button_box >= 150] = 1
        # plt.imshow(game_over)


        if not_zero >= 90 and not_zero <= 160 and np.sum(game_over_button) > 600:
            self.press_space()
            self.time_jump = self.init_values['time_jump']
            self.wait = self.init_values['wait']
            self.coord_jump = self.init_values['coord_jump'].copy()
            self.coord_gameover = self.init_values['coord_gameover'].copy()
            self.image = np.zeros((500, 500))
            print('RESTART')


    def jump(self):
        img_jump_box = self.image[self.coord_jump[0]:self.coord_jump[2],
                                  self.coord_jump[1]:self.coord_jump[3]]
        img_jump = img_jump_box.copy()
        img_jump[img_jump_box < 165] = 0
        img_jump[img_jump_box >= 165] = 1

        # plt.imshow(img_jump)

        if(np.sum(img_jump) > 100):
            self.coord_jump[3] = np.clip(self.coord_jump[3] + 1, 145, 250)
            self.time_jump = np.clip(self.time_jump - 0.0015, 0.03, 0.3)
            self.wait = np.clip(self.wait - 0.00025, 0.005, 1)
            self.press_space()

            print(f'PULOU: {self.coord_jump[3]}   {self.time_jump :.4f}    {self.wait :.6f} ')
