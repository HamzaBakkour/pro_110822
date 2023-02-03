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


    #Start the listner with argg
    def _start_shortcut_listener(self, argg):
        if (len(argg) > 0):
            self._shortcutListner =  keyboard.GlobalHotKeys(eval(argg))
            self._shortcutListner.start()
        else:
            print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', 'Empty argument passed to _shortcutListner')

    #Stop the listner and restart it with argg
    def _refresh_shortcut_listener(self, argg):
        if (len(argg) > 0):
            self._shortcutListner.stop()
            self._shortcutListner =  keyboard.GlobalHotKeys(eval(argg))
            self._shortcutListner.start()
        else:
            print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', 'Empty argument passed to _refresh_shortcut_lister')
    
    #Stop the listner
    def _stop_shortcut_listener(self):
        self._shortcutListner.stop()





    def define_shortcut(self,*args : str,  addToExist: bool = False, passShortcut = False) -> None:
        print('///////////////////////////////////////////////////////////////////////////////////')
######################################################################################################################################################################################
        #args: list[(str, str)], the arguemnt passed when the method is called.
        #self._onShortcutActivateArgument: list[(str, str)], the shortcuts that are currently in use.
        if (len(args) == 0):
            if self._shortcutListner:
                self._stop_shortcut_listner()
            return
        elif (addToExist == True):
            #args.extend(self._onShortcutActivateArgument) -> AttributeError: 'tuple' object has no attribute 'extend'
            args = list(args)
            args.extend(self._onShortcutActivateArgument)
        else:
            self._onShortcutActivateArgument = []
            self._onShortcutActivateArgument.extend(args)
########################################################################################################################################################################################







######################################################################################### argg #########################################################################################
        #argg: list, is the argument passed to self._shortcutListner
        argg = '{'
        for _ in range(len(args)):
            print(f'--------------------------\nHandeling arg : {args[_]}\nWhere args[_][0][-4:] is {args[_][0][-4:]}\nAnd args[_][0][-5:] is {args[_][0][-5:]}\nAnd len(args[_]) is {len(args[_])}\nAnd passShortcut is {passShortcut}\n--------------------------')
            print(f'argg : {argg}\nargs : {args}\nself._onShortcutActivateArgument : {self._onShortcutActivateArgument}\n--------------------------')
            
            if (len(args[_]) == 2 and (args[_][0][-4:] == 'PASS')):
                print('[1]')
                argg = argg + "'" + args[_][0][:-4] + "'" + ':' + f' lambda self = self : self.calledObject.{args[_][1]}(\'{args[_][0][:-4]}\')' + ', '
            elif (len(args[_]) == 2 and (args[_][0][-5:] == 'DONOT')):
                print('[2]')
                argg = argg + "'" + args[_][0][:-5] + "'" + ':' + f' lambda self = self : self.calledObject.{args[_][1]}()' + ', '
            elif (len(args[_]) == 2 and (passShortcut)):
                print('[3]')
                argg = argg + "'" + args[_][0] + "'" + ':' + f' lambda self = self : self.calledObject.{args[_][1]}(\'{args[_][0]}\')' + ', '
            elif (len(args[_]) == 2 and (not passShortcut)):
                print('[4]')
                argg = argg + "'" + args[_][0] + "'" + ':' + f' lambda self = self : self.calledObject.{args[_][1]}()' + ', '
            elif(len(args[_]) > 2) :
                print('[5]')
                if(passShortcut):
                    calledObejectMethodArgs = f'\'{args[_][0]}\', '
                else:
                    calledObejectMethodArgs = ''
                for el in range(2, len(args[_])):
                    calledObejectMethodArgs = calledObejectMethodArgs + f'{args[_][el]} ,'
                calledObejectMethodArgs = calledObejectMethodArgs[:-2]
                argg = argg + "'" + args[_][0] + "'" + ':' + f' lambda self = self : self.calledObject.{args[_][1]}({calledObejectMethodArgs})' + ', '
            else:
                print('[6]')
                print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', f'{args} is invalied argument.')
                return
        argg = argg[:-2] + '}'
######################################################################################################################################################################################
  





############### loop through a list of tuples and append a value ####################################################################################################################
        args = list(args)
        for index, _ in enumerate(args):
            if(passShortcut):
                print('L1')
                temp=list(args[index])
                print(temp[0])
                if (temp[0][-4:] == 'PASS'):
                    print('L1.1')
                    pass
                elif (temp[0][-5:] == 'DONOT'):
                    print('L1.2')
                    pass
                else:
                    print('L1.3')
                    temp[0] = temp[0] + 'PASS'
                args[index]=tuple(temp)
            else:
                print('L2')
                temp=list(args[index])
                print(temp[0])
                if (temp[0][-5:] == 'DONOT'):
                    print('L2.1')
                    pass
                if (temp[0][-4:] == 'PASS'):
                    print('L2.2')
                    pass       
                else:
                    print('L2.3')
                    temp[0] = temp[0] + 'DONOT'
                args[index]=tuple(temp)

        self._onShortcutActivateArgument = []
        for item in args:
            if (item not in self._onShortcutActivateArgument):
                self._onShortcutActivateArgument.append(item)


        print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', f'after loop, args is : {args}')
        print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', f'after loop, self._onShortcutActivateArgument is : {self._onShortcutActivateArgument}')

         
######################################################################################################################################################################################


        if self._shortcutListner:
            self._refresh_shortcut_listener(argg)
            print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', f'Started shortcut listener with argument : {argg} [Refresh]')
        else:
            self._start_shortcut_listener(argg)
            print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', f'Started shortcut listener with argument : {argg} [-]')


        print('///////////////////////////////////////////////////////////////////////////////////')

    def remove_shortcut(self, shortcut: str)->None:
        try:
            for el in self._onShortcutActivateArgument:
                if (el[0] == shortcut):
                    self._onShortcutActivateArgument.remove(el)
        except Exception as ex:
            print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', f'Exception raised : {ex}')
            return
















































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




