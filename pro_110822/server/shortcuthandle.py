from pynput import keyboard
import inspect
from prologging import Log
import os
import pdb

class ShortcutsHandle():
    
    def __init__(self, calledObject):
        self._shortcutListener = False
        self._savedShortcuts = []
        self._log = Log()
        self.calledObject = calledObject

    def _start_shortcut_listener(self, argg):
        if (len(argg) > 0):
            self._shortcutListener =  keyboard.GlobalHotKeys(eval(argg))
            self._shortcutListener.start()
        else:
            print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', 'Empty argument passed to _shortcutListner')

    def _refresh_shortcut_listener(self, argg):
        if (len(argg) > 0):
            self._shortcutListener.stop()
            self._log.info(['_refresh_shortcut_listener'],
                           message=f'argg:{argg}')
            self._shortcutListener =  keyboard.GlobalHotKeys(eval(argg))
            self._shortcutListener.start()
        else:
            print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', 'Empty argument passed to _refresh_shortcut_lister')
    
    def _stop_shortcut_listener(self):
        self._shortcutListener.stop()

    def define_shortcut(self,*args : list[tuple[str, str]],  addToExist=True, passShortcut=True) -> None:
        self._log.info(['define_shortcut'],
                       message=f'called with args:{args}')

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
            self._log.info(['define_shortcut'],
                            message=f'Started shortcut listener with argument : {argg} [Refresh]')
        else:
            self._start_shortcut_listener(argg)
            self._log.info(['define_shortcut'],
                           message=f'Started shortcut listener with argument : {argg} [-]')

    def remove_shortcut(self, shortcut: str)->bool:
        was_removed = False
        temp_list = self._savedShortcuts
        # print(f'save: {self._savedShortcuts}')

        # pdb.set_trace()
        try:
            for el in temp_list:
                if (el[0] == shortcut + 'PASS' or el[0] == shortcut + 'DONOT'):
                    temp_list.remove(el)
                    was_removed = True
        except Exception as ex:
            print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', f'Exception raised : {ex}')
            return was_removed

        if len(temp_list) > 1:
            if temp_list[0][0][-4:] == 'PASS':
                self.define_shortcut((temp_list[0][0].replace('PASS', ''),
                                      temp_list[0][1]), 
                                     addToExist=False, 
                                     passShortcut=True)

            elif temp_list[0][0][-5:] == 'DONOT':
                self.define_shortcut((temp_list[0][0].replace('DONOT', ''),
                                      temp_list[0][1]), 
                                     addToExist=False, 
                                     passShortcut=True)

            # pdb.set_trace()
            
            for el in temp_list[1:]:
                if el[0][-4:] == 'PASS':
                    self.define_shortcut((el[0].replace('PASS', ''),
                                          el[1]), 
                                        addToExist=True, 
                                        passShortcut=True)

                elif el[0][-5:] == 'DONOT':
                    self.define_shortcut((el[0].replace('DONOT', ''),
                                          el[1]), 
                                        addToExist=True, 
                                        passShortcut=True)


        self._log.info(['remove_shortcut'],
                       message=f'after remove, _savedShortcuts:{self._savedShortcuts}')
        return was_removed

    def remove_all_shortcuts(self):
        self._log.info(['remove_all_shortcuts'],
                       message='REMOVING ALL SHORTCUTS')
        for shortcut_ in self._savedShortcuts:
            # pdb.set_trace()
            if shortcut_[0][-4:] == 'PASS':
                self.remove_shortcut(shortcut_[0].replace('PASS', ''))
            elif shortcut_[0][-5:] == 'DONOT':
                self.remove_shortcut(shortcut_[0].replace('DONOT', ''))

        self._log.info(['remove_all_shortcuts'],
                       message=f'123123 _savedShortcuts:{self._savedShortcuts}')

        # self._stop_shortcut_listener()

    def refresh(self):
        
        self._log.info(['refresh'],
                       message='REFRESHING')
        _shortcuts =  []

        for _shortcut in self._savedShortcuts:
            if _shortcut[0][-4:] == 'PASS':
                _shortcuts.append((_shortcut[0][:-4], _shortcut[1]))

            elif _shortcut[0][-5:] == 'DONOT':
                _shortcuts.append((_shortcut[0][:-5], _shortcut[1]))
                
        self._log.info(['refresh'],
                       message='calling remove_all_shortcuts')
        
        self.remove_all_shortcuts()
        
        self._log.info(['refresh'],
                        message=f'calling define_shortcut with _shortcuts:{_shortcuts}')
        
        
        for _shortcut in _shortcuts:
            self.define_shortcut(_shortcut, addToExist=True, passShortcut=True)
        
        self._log.info(['refresh'],
                        message='REDEFINED shortcuts [DONE]')
