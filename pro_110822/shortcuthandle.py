from pynput import keyboard
import inspect
import os


class ShortcutsHandle():
    """Define a shortcut and a method to ba called when the shortcut is pressed"""
    def __init__(self, calledObject):
        self._shortcutListener = False
        self._savedShortcuts = []
        self.calledObject = calledObject

    #Start the listener.
    def _start_shortcut_listener(self, argg):
        if (len(argg) > 0):
            self._shortcutListener =  keyboard.GlobalHotKeys(eval(argg))
            self._shortcutListener.start()
        else:
            print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', 'Empty argument passed to _shortcutListner')


    #Stop the listener and restart it.
    def _refresh_shortcut_listener(self, argg):
        if (len(argg) > 0):
            self._shortcutListener.stop()
            self._shortcutListener =  keyboard.GlobalHotKeys(eval(argg))
            self._shortcutListener.start()
        else:
            print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', 'Empty argument passed to _refresh_shortcut_lister')
    
    #Stop the listner.
    def _stop_shortcut_listener(self):
        self._shortcutListener.stop()


    #Define the shortcuts that the listener will listen to.
    def define_shortcut(self,*args : list[tuple[str, str]],  addToExist: bool = False, passShortcut = False) -> None:
        """Define a shortcut.
        
        Examples:
            >>> class HelloClass():
            ...     def hello_method(self, message):
            ...         print(f'Hello there! You are here because the shortcut {message} was pressed!')
            >>> Hello = HelloClass()
            >>> Shortcut = ShortcutsHandle(Hello)
            >>> Shortcut.define_shortcut(('<ctrl>+x', 'hello_method'), passShortcut = True)
            shortcuthandle.py |  define_shortcut |  <module> ||  Started shortcut listener with argument : {'<ctrl>+x': lambda self = self : self.calledObject.hello_method('<ctrl>+x')} [-]
            >>> from pynput.keyboard import Key, Controller
            >>> keyboard = Controller()
            >>> keyboard.press(Key.ctrl)
            >>> keyboard.press('x')
            >>> import time
            >>> time.sleep(0.1)
            Hello there! You are here because the shortcut <ctrl>+x was pressed!
            >>> keyboard.release(Key.ctrl)
            >>> keyboard.release('x')
            >>> Shortcut.remove_shortcut('<ctrl>+x')
            >>> keyboard.press(Key.ctrl)
            >>> keyboard.press('x')
            >>> time.sleep(0.1)
            >>> keyboard.release(Key.ctrl)
            >>> keyboard.release('x')

        Args:
            *args (list[tuple[str, str]): The first element in the tuple is the shortcut. The second element is the method to be called when the shortcut is pressed.
            addToExist (bool) : If true, the passed shortcuts are added to any existing shortcuts
                                If false, any existing shortcuts are removed and the passed shortcuts are defined
            passShortcut (bool) : If true, the pressed shortcut is passed to the method to be called when the shortcut is pressed.
                                    PS: Its not possible to pass any arguemnts - other than the pressed shortcut - to the method to be called when the shortcut is pressed.
                                        This will be fixed in the future.

        Returns:
            None

        """
        #args: list[(str, str)], the arguemnt passed when the method is called.
        #self._savedShortcuts: list[(str, str)], the shortcuts that are currently in use.
        if (len(args) == 0):
            if self._shortcutListener:
                self._stop_shortcut_listener()
            return
        elif (addToExist == True):
            #changin args from tuple -> list
            #adding the existing saved shortcuts to the passed shortcuts (args)
            args = list(args)
            args.extend(self._savedShortcuts)
        else:
            self._savedShortcuts = []
            self._savedShortcuts.extend(args)


        argg = '{' #argg: list, is the argument passed to self._shortcutListner
        for _ in range(len(args)):
            #each element in args is of the form: element(shortcut: str, function: str')
            if (len(args[_]) == 2 and (args[_][0][-4:] == 'PASS')):#if the last four latters in the shortcut string == 'PASS' -> #call lambda and pass the shortcut
                argg = argg + "'" + args[_][0][:-4] + "'" + ':' + f' lambda self = self : self.calledObject.{args[_][1]}(\'{args[_][0][:-4]}\')' + ', '
            
            elif (len(args[_]) == 2 and (args[_][0][-5:] == 'DONOT')):#if the last five latters in the shortcut string == 'DONOT' -> #call lambda and pass the shortcut                                      
                argg = argg + "'" + args[_][0][:-5] + "'" + ':' + f' lambda self = self : self.calledObject.{args[_][1]}()' + ', '
            
            elif (len(args[_]) == 2 and (passShortcut)):#if the passed shortcut string does not end with neither 'PASS' nor 'DONOT' #and passShortcut -> #call lambda and pass the shortcut  
                argg = argg + "'" + args[_][0] + "'" + ':' + f' lambda self = self : self.calledObject.{args[_][1]}(\'{args[_][0]}\')' + ', '

            elif (len(args[_]) == 2 and (not passShortcut)):#if the passed shortcut string does not end with neither 'PASS' nor 'DONOT' #and not passShortcut -> #call lambda and do not pass the shortcut  
                argg = argg + "'" + args[_][0] + "'" + ':' + f' lambda self = self : self.calledObject.{args[_][1]}()' + ', '
            else:
                print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', f'{args} is invalied argument.')
                return
        argg = argg[:-2] + '}'
  
        #iterate through each passed argument #if passShortcut -> #add 'PASS' to the end of the shortcut (if it does not have neither 'PASS' nor 'DONOT')
                                                #else -> add 'DONOT' (if it does not have neither 'PASS' nor 'DONOT')
        args = list(args)
        for index, _ in enumerate(args):
            if(passShortcut):
                temp=list(args[index])
                if (temp[0][-4:] == 'PASS' or temp[0][-5:] == 'DONOT'):
                    pass
                else:
                    temp[0] = temp[0] + 'PASS'
                args[index]=tuple(temp)
            else:
                temp=list(args[index])
                if (temp[0][-5:] == 'DONOT' or temp[0][-4:] == 'PASS'):
                    pass
                else:
                    temp[0] = temp[0] + 'DONOT'
                args[index]=tuple(temp)

        #if the method is called with passShortcut -> args allready has the shortcuts in self._savedShortcuts -> #its safe to: self._savedShortcuts = []
        #if the method is called with passShortcut = False -> self._savedShortcuts is emptyd and the shortcuts in args are added to it.
        self._savedShortcuts = []
        for item in args:
            if (item not in self._savedShortcuts):
                self._savedShortcuts.append(item)


        if self._shortcutListener:
            self._refresh_shortcut_listener(argg)
            print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', f'Started shortcut listener with argument : {argg} [Refresh]')
        else:
            self._start_shortcut_listener(argg)
            print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', f'Started shortcut listener with argument : {argg} [-]')


    def remove_shortcut(self, shortcut: str)->None:
        """"Remove a shortcut. The listener will stop listning to the removed shortcut"""
        try:
            for el in self._savedShortcuts:
                if (el[0] == shortcut + 'PASS' or el[0] == shortcut + 'DONOT'):
                    self._savedShortcuts.remove(el)
        except Exception as ex:
            print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', f'Exception raised : {ex}')
            return

        self.define_shortcut(*self._savedShortcuts, addToExist=False, passShortcut=True)












    # print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', f'after loop, args is : {args}')
    # print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', f'after loop, self._onShortcutActivateArgument is : {self._onShortcutActivateArgument}')

    # print(f'--------------------------\nHandeling arg : {args[_]}\nWhere args[_][0][-4:] is {args[_][0][-4:]}\nAnd args[_][0][-5:] is {args[_][0][-5:]}\nAnd len(args[_]) is {len(args[_])}\nAnd passShortcut is {passShortcut}\n--------------------------')
    # print(f'argg : {argg}\nargs : {args}\nself._onShortcutActivateArgument : {self._onShortcutActivateArgument}\n--------------------------')

    # elif(len(args[_]) > 2) :#if additional arguments are passed #additional arguments are more than two arguments - the shortcut and the function to be called when the shortcut is pressed - are passed -
    #                           #->the additional argumnts are passed to the function to be called when the shortcut is pressed
    #     if(passShortcut):
    #         calledObejectMethodArgs = f'\'{args[_][0]}\', '
    #     else:
    #         calledObejectMethodArgs = ''
    #     for el in range(2, len(args[_])):
    #         calledObejectMethodArgs = calledObejectMethodArgs + f'{args[_][el]} ,'
    #     calledObejectMethodArgs = calledObejectMethodArgs[:-2]
    #     argg = argg + "'" + args[_][0] + "'" + ':' + f' lambda self = self : self.calledObject.{args[_][1]}({calledObejectMethodArgs})' + ', '

    # def on_shortcut_activate(self, m : str)-> None:
    #     """
    #     This method is called when a shortcut is pressed.  
    #     Shortcuts are defind by the method define_shortcuts(self,*args, addToExist = False)

    #     Args:
    #         m: The shortcut that has been pressed by the user.

    #     Retursn:
    #         None
    #     """
    #     print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', f'shortcut detected >>> {m}')
    #     #Server shortcut
    #     if(m == '<ctrl>+m+1'):
    #         self.sendUserInput.supress_user_input(False)
    #         self.sendUserInput.send_input_to_client(None)
    #     else:#Client shortcut
    #         self.sendUserInput.supress_user_input(True)
    #         try:
    #             self.sendUserInput.send_input_to_client(self.clientsConnections[int(m[-1]) - 2])
    #         except Exception as ex:
    #             print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', f'Exception raisde {ex}')


    # def define_shortcuts(self,*args : str, addToExist: bool = False) -> None:
    #     """
    #     Define shortcuts.  

    #     Args:
    #         *args[str]: Shortcuts that the listner will listen to.
    #         addToExist: If True, the shortcuts defined by args will be added to the existing shortcuts.  
    #                     If False,  any existing shortcuts will be removed and the shortcuts defined by args will be added.

    #     Returns:
    #         None
    #     """
    #     print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', f'args: {args}')
    #     if (len(args) == 0):
    #         if self.shortcutListner:
    #             self.onShortcutActivateArgument = []
    #             self.shortcutListner.stop()
    #         return
    #     if (addToExist == False):
    #         argg = '{'
    #         for _ in range(len(args)):
    #             # try:
    #             argg = argg + "'" + args[_] + "'" + ':' + ' lambda self = self : self.on_shortcut_activate({})'.format("'" + args[_] + "'") + ', '

    #         argg = argg[:-2] + '}'
    #         self.onShortcutActivateArgument = []
    #         self.onShortcutActivateArgument.extend(args)
    #     elif (addToExist == True):
    #         args = list(args)
    #         args.extend(self.onShortcutActivateArgument)
    #         argg = '{'
    #         for _ in range(len(args)):
    #             argg = argg + "'" + args[_] + "'" + ':' + ' lambda self = self : self.on_shortcut_activate({})'.format("'" + args[_] + "'") + ', '
    #         argg = argg[:-2] + '}'
    #         self.onShortcutActivateArgument = []
    #         self.onShortcutActivateArgument.extend(args)
    #     print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', '_define_shortcuts / args :', args)
    #     if self.shortcutListner:
    #         self.shortcutListner.stop()
    #         self.shortcutListner =  keyboard.GlobalHotKeys(eval(argg))
    #         self.shortcutListner.start()
    #     else:
    #         self.shortcutListner =  keyboard.GlobalHotKeys(eval(argg))
    #         self.shortcutListner.start()




