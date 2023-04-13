from prologging import Log
# from shortcuthandle import ShortcutsHandle
from pynput import keyboard
import time


class TestClass():
    def __init__(self) -> None:
        self._log = Log()
        self._listener = None
        self._current_shortcuts = []

    def boo(self, shortcut):
        self._log.debug(['boo'],
                       message=f'called with shortcut:{shortcut}')

    def _update_listener(self):
            self._log.info(['_update_listener'],
                            message='...')
            
            if self._listener != None:
                self._stop_listener()


            self._log.info(['_update_listener'],
                           message='UPDATING')
            

            argument = '{'
            for shortcut in self._current_shortcuts:
                argument = argument + f"'{shortcut['shortcut']}' : lambda self = self : {shortcut['target_function']}('{shortcut['shortcut']}'), "
            
            argument = argument[:-2]

            argument += '}'

            self._log.info(['_update_listener'],
                           message=f'listener argument:{argument}')

            self._listener = keyboard.GlobalHotKeys(eval(argument))


            self._listener.start()
    
    def define_shortcut(self, shortcut, target_function,  add_to_existing=True) -> None:
        self._log.info(['define_shortcut'],
                       message=f'called with shortcut:{shortcut}, target_function:{target_function}, add_to_existing:{add_to_existing}')


        if add_to_existing:
            self._log.info(['define_shortcut'],
                            message=f'UPDATING listener with:{self._current_shortcuts}')
            self._current_shortcuts.append({'shortcut' : shortcut, 'target_function' : target_function, 'add_to_existing' : add_to_existing})
            self._update_listener()
            return

        self._current_shortcuts = []
        self._current_shortcuts.append({'shortcut' : shortcut, 'target_function' : target_function, 'add_to_existing' : add_to_existing})
        if self._listener != None:
            self._stop_listener()



        listener_argument = f"{{'{shortcut}' : lambda self = self : {target_function}('{shortcut}')}}"

        self._listener =  keyboard.GlobalHotKeys(eval(listener_argument))

        self._listener.start()
        self._log.info(['define_shortcut'],
                        message=f'Started shortcut listener with argument : {listener_argument}[-]')

    def remove_shortcut(self, to_be_removed: str)->bool:
        was_removed = False

        for shortcut in  self._current_shortcuts:
            if shortcut['shortcut'] == to_be_removed:
                self._current_shortcuts.remove(shortcut)

        temp = self._current_shortcuts
        self._current_shortcuts = []

        if len(temp) > 1 :
            self.define_shortcut(temp[0]['shortcut'], 
                                 temp[0]['target_function'],
                                 add_to_existing=False)
            
            for shortcut in temp[1:]:
                self.define_shortcut(shortcut['shortcut'],
                                     shortcut['target_function'],
                                     add_to_existing=True)
            was_removed = True

        else:
            self.define_shortcut(temp[0]['shortcut'], 
                                 temp[0]['target_function'],
                                 add_to_existing=False)
            was_removed = True

        return was_removed

    def remove_all_shortcuts(self):
        self._log.info(['remove_all_shortcuts'],
                       message='REMOVING ALL SHORTCUTS')
        self._current_shortcuts = []
        self._stop_listener()

    def _stop_listener(self):
        self._log.info(['stop_listener'],
                       message='STOPPING >')
        if self._listener != None:
            self._listener.stop()
            self._listener.join()
            self._listener = None
            time.sleep(0.1) 
            self._log.info(['stop_listener'],
                        message='STOPPING >> STOPPED')
        else:
            self._log.info(['stop_listener'],
                        message='STOPPING >> listener is ALREADY STOPED')

    def refresh_shortcuts(self):
        self._log.info(['refresh'],
                       message='REFRESHING')
        
        temp = self._current_shortcuts
        self.remove_all_shortcuts()

        if len(temp) > 1:
            self.define_shortcut(temp[0]['shortcut'],
                                 temp[0]['target_function'],
                                 add_to_existing=False)
            
            for shortcut in temp[1:]:
                self.define_shortcut(shortcut['shortcut'],
                                    shortcut['target_function'],
                                    add_to_existing=True)
            self._log.info(['refresh'],
                            message='REDEFINED shortcuts [DONE]')
            return
        

        self.define_shortcut(temp[0]['shortcut'],
                                temp[0]['target_function'],
                                add_to_existing=False)
        self._log.info(['refresh'],
                        message='REDEFINED shortcuts [DONE]')



        # self._current_shortcuts.append({'shortcut' : shortcut, 'target_function' : target_function, 'add_to_existing' : add_to_existing})


        # self._savedShortcuts = []
        # for item in args:
        #     if item not in self._savedShortcuts:
        #         self._savedShortcuts.append(item)


# t = TestClass()





# t.define_shortcut('<ctrl>+m+1', 
#                         'self.boo')


# t.define_shortcut('<ctrl>+m+2', 
#                         'self.boo')


# t.define_shortcut('<ctrl>+m+4', 
#                         'self.boo')

# print('first sleep')#############################################################
# time.sleep(10)

# t.remove_shortcut('<ctrl>+m+1')


# print('second sleep')#############################################################
# time.sleep(10)


# t.refresh()


# print('therd sleep')#############################################################
# time.sleep(10)


# t.remove_shortcut('<ctrl>+m+2')


# print('fourth sleep')#############################################################
# time.sleep(10)



# t.remove_all_shortcuts()


# print('fifth sleep')#############################################################
# time.sleep(10)




# self.define_shortcut('<ctrl>+m+2', 
#                       'self.boo', 
#                       add_to_existing=True,)
# self.semi_boo()


# print('first sleep')
# time.sleep(10)


# t.define_shortcut('<ctrl>+m+4', 
#                   'self.boo',
#                   add_to_existing=False)

# print('second sleep')
# time.sleep(10)

# t.define_shortcut('<ctrl>+m+1', 
#                   'self.boo')

# print('therd sleep')
# time.sleep(10)


# t.semi_boo_1()
# print('second sleep')
# time.sleep(10)
# print('third sleep')
# t.remove_all_shortcuts()
# time.sleep(30)







    # def _stop_shortcut_listener(self):
    #     if self._listener != None:
    #         self._log.info(['_stop_shortcut_listener'],
    #                        message='STOPPING')
    #         self._listener.stop()
    #         self._listener.join()
    #         return

    #     self._log.info(['_stop_shortcut_listener'],
    #                     message='listener is None -> RETURNING')




        # temp_list = self._current_shortcuts
        # # print(f'save: {self._savedShortcuts}')

        # # pdb.set_trace()

        # try:
        #     for el in temp_list:
        #         if (el[0] == shortcut + 'PASS' or el[0] == shortcut + 'DONOT'):
        #             temp_list.remove(el)
        #             was_removed = True
        # except Exception as ex:
        #     print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', f'Exception raised : {ex}')
        #     return was_removed

        # if len(temp_list) > 1:
        #     if temp_list[0][0][-4:] == 'PASS':
        #         self.define_shortcut((temp_list[0][0].replace('PASS', ''),
        #                               temp_list[0][1]), 
        #                              add_to_existing=False, 
        #                              pass_shortcut=True)

        #     elif temp_list[0][0][-5:] == 'DONOT':
        #         self.define_shortcut((temp_list[0][0].replace('DONOT', ''),
        #                               temp_list[0][1]), 
        #                              add_to_existing=False, 
        #                              pass_shortcut=True)

        #     for el in temp_list[1:]:
        #         if el[0][-4:] == 'PASS':
        #             self.define_shortcut((el[0].replace('PASS', ''),
        #                                   el[1]), 
        #                                 add_to_existing=True, 
        #                                 pass_shortcut=True)

        #         elif el[0][-5:] == 'DONOT':
        #             self.define_shortcut((el[0].replace('DONOT', ''),
        #                                   el[1]), 
        #                                 add_to_existing=True, 
        #                                 pass_shortcut=True)


        # self._log.info(['remove_shortcut'],
        #                message=f'after remove, _savedShortcuts:{self._current_shortcuts}')