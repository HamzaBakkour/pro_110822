from pynput import keyboard
import inspect
import os

# in this module, 
#   you define the shortcut and the function to be called 
#       when the shortcut is pressed
#   Tihs is done in form of tuples,
#       the first element in the tuple is the shortcut
#       the second element in the tuple is the function    

class ShortcutsHandle():

    def __init__(self, calledObject):
        self._shortcutListner = False
        self._onShortcutActivateArgument = []
        self.calledObject = calledObject


    def _start_shortcut_listener(self, argg):
        if (len(argg) > 0):
            self._shortcutListner =  keyboard.GlobalHotKeys(eval(argg))
            self._shortcutListner.start()
        else:
            print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', 'Empty argument passed to _shortcutListner')


    def _refresh_shortcut_listener(self, argg):
        if (len(argg) > 0):
            self._shortcutListner.stop()
            self._shortcutListner =  keyboard.GlobalHotKeys(eval(argg))
            self._shortcutListner.start()
        else:
            print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', 'Empty argument passed to _refresh_shortcut_lister')
    
    
    def _stop_shortcut_listener(self):
        self._shortcutListner.stop()

    def define_shortcut(self,*args : str,  addToExist: bool = False, passShortcut = False) -> None:

        if (len(args) == 0):
            if self._shortcutListner:
                self._stop_shortcut_listner()
            return

        if (addToExist == True):
            args = list(args)
            args.extend(self._onShortcutActivateArgument)

        argg = '{'
        for _ in range(len(args)):
            if (len(args[_]) == 2 and (passShortcut)):
                argg = argg + "'" + args[_][0] + "'" + ':' + f' lambda self = self : self.calledObject.{args[_][1]}(\'{args[_][0]}\')' + ', '
            elif (len(args[_]) == 2):
                argg = argg + "'" + args[_][0] + "'" + ':' + f' lambda self = self : self.calledObject.{args[_][1]}()' + ', '
            elif(len(args[_]) > 2) :
                if(passShortcut):
                    calledObejectMethodArgs = f'\'{args[_][0]}\', '
                else:
                    calledObejectMethodArgs = ''

                for el in range(2, len(args[_])):
                    calledObejectMethodArgs = calledObejectMethodArgs + f'{args[_][el]} ,'
                calledObejectMethodArgs = calledObejectMethodArgs[:-2]
                argg = argg + "'" + args[_][0] + "'" + ':' + f' lambda self = self : self.calledObject.{args[_][1]}({calledObejectMethodArgs})' + ', '
            
            else:
                print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', f'{args} is invalied argument.')
                return

        
        argg = argg[:-2] + '}'
        self._onShortcutActivateArgument = []
        self._onShortcutActivateArgument.extend(args)


        if self._shortcutListner:
            self._refresh_shortcut_listener(argg)
            print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', f'Started shortcut listener with argument : {argg} [Refresh]')
        else:
            self._start_shortcut_listener(argg)
            print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', f'Started shortcut listener with argument : {argg} [-]')
























































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




