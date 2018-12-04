# ======================================================================
# FILE:        MyAI.py
#
# AUTHOR:      Abdullah Younis
#
# DESCRIPTION: This file contains your agent class, which you will
#              implement. You are responsible for implementing the
#              'getAction' function and any helper methods you feel you
#              need.
#
# NOTES:       - If you are having trouble understanding how the shell
#                works, look at the other parts of the code, as well as
#                the documentation.
#
#              - You are only allowed to make changes to this portion of
#                the code. Any changes to other portions of the code will
#                be lost when the tournament runs your code.
# ======================================================================

from Agent import Agent

class MyAI ( Agent ):

    def __init__ ( self ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================

        self.on_main=True
        self.on_part=False
        self.main_meet=False
        self.part_meet=False
        self.main_count=0
        self.part_count=0
        self.part_back_mode =False
        self.main_back_mode=False
        self.getgoal=False
        self.monsteralive = True
        self.shooted = False
        self.justshooted = False
        self.finishfirstsearch = False
        self.main_breeze = False
        self.main_bump = False
        self.at_beginning = True
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    def getAction( self, stench, breeze, glitter, bump, scream ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        # Print Command Menu
        if(self.at_beginning):
            if(breeze):
                return Agent.Action.CLIMB
            else:
                self.at_beginning = False

        if(scream):
            self.monsteralive = False

        if not self.finishfirstsearch:
            if glitter:
                self.getgoal=True
                return Agent.Action.GRAB
            if self.getgoal==True:
                if self.on_main:
                    if self.main_back_mode==True:
                        if self.main_count!=0:
                            self.main_count-=1
                            return Agent.Action.FORWARD
                        else:
                            return Agent.Action.CLIMB
                    else:
                        if self.main_meet==False:
                            self.main_meet=True
                            return Agent.Action.TURN_LEFT
                        else:
                            self.main_back_mode=True
                            return Agent.Action.TURN_LEFT
                else:
                    if self.part_back_mode==True:
                        if self.part_count!=0:
                            self.part_count-=1
                            return Agent.Action.FORWARD
                        else:
                            self.on_main=True
                            return Agent.Action.TURN_RIGHT
                    else:
                        if self.part_meet==False:
                            self.part_meet=True
                            return Agent.Action.TURN_LEFT
                        else:
                            self.part_back_mode=True
                            return Agent.Action.TURN_LEFT
            if self.main_meet==False:
                if (not stench and not breeze and not bump):
                    self.main_count+=1
                    return Agent.Action.FORWARD
                else:
                    if (breeze):
                        if(self.main_breeze):
                            pass
                        else:
                            self.main_breeze = True
                            self.main_meet = True
                            return Agent.Action.TURN_LEFT
                    elif (bump):
                        self.main_count -= 1
                        self.main_bump = True
                        self.main_meet = True
                        self.main_back_mode = True

                        self.on_main = False
                        self.on_part = True
                        self.part_back_mode = False
                        self.part_meet = False
                        self.part_count = 0
                        return Agent.Action.TURN_LEFT
                    else:
                        if(self.monsteralive):
                                if (self.justshooted):
                                    self.justshooted = False
                                    self.main_count+=1
                                    return Agent.Action.FORWARD
                                else:
                                    if (self.shooted):
                                        self.main_meet = True
                                        return Agent.Action.TURN_LEFT
                                    else:
                                        self.shooted = True
                                        self.justshooted = True
                                        return Agent.Action.SHOOT
                        else:
                            self.main_count+=1
                            return Agent.Action.FORWARD
            if self.main_back_mode==False:
                self.main_back_mode = True
                return Agent.Action.TURN_LEFT
            if self.on_main==True:
                if self.main_count!=0:
                    if(self.main_breeze):
                        self.main_breeze = False
                        self.main_count -= 1
                        return Agent.Action.FORWARD
                    elif(stench):
                        if(self.monsteralive):
                            self.main_count -= 1
                            return Agent.Action.FORWARD
                        else:
                            self.on_main = False
                            self.on_part = True
                            self.part_back_mode = False
                            self.part_meet = False
                            self.part_count = 0
                            return Agent.Action.TURN_RIGHT
                    else:
                        self.on_main=False
                        self.on_part=True
                        self.part_back_mode=False
                        self.part_meet=False
                        self.part_count=0
                        return Agent.Action.TURN_RIGHT
                else:
                    self.finishfirstsearch = True
                    self.on_main=True
                    self.on_part=False
                    self.main_meet=False
                    self.part_meet=False
                    self.main_count=0
                    self.part_count=0
                    self.part_back_mode =False
                    self.main_back_mode=False
                    return Agent.Action.TURN_RIGHT
            if self.part_back_mode==False:
                if self.part_meet==False:
                    if (not stench and not breeze and not bump):
                       self.part_count += 1
                       return Agent.Action.FORWARD

                    else:
                        if (breeze):
                            self.part_meet = True
                            return Agent.Action.TURN_LEFT
                        elif(bump):
                            self.part_count -= 1
                            self.part_meet = True
                            return Agent.Action.TURN_LEFT
                        else:
                            if (self.monsteralive):
                                if (self.justshooted):
                                    self.justshooted = False
                                    self.part_count+= 1
                                    return Agent.Action.FORWARD
                                else:
                                    if (self.shooted):
                                        self.part_meet = True
                                        return Agent.Action.TURN_LEFT
                                    else:
                                        self.shooted = True
                                        self.justshooted = True
                                        return Agent.Action.SHOOT
                            else:
                                self.part_count += 1
                                return Agent.Action.FORWARD

                else:
                    self.part_back_mode=True
                    return Agent.Action.TURN_LEFT
            else:
                if self.part_count!=0:
                    self.part_count-=1
                    return Agent.Action.FORWARD
                else:
                    if self.on_part==True:
                        self.on_part=False
                        return Agent.Action.TURN_RIGHT
                    elif self.main_count!=0:
                        self.main_count-=1
                        self.on_main=True
                        return Agent.Action.FORWARD
                    elif self.getgoal==True:
                        return Agent.Action.CLIMB
                    else:
                        self.finishfirstsearch = True
                        self.on_main=True
                        self.on_part=False
                        self.main_meet=False
                        self.part_meet=False
                        self.main_count=0
                        self.part_count=0
                        self.part_back_mode =False
                        self.main_back_mode=False
                        return Agent.Action.TURN_RIGHT
        else:
            if glitter:
                self.getgoal=True
                return Agent.Action.GRAB
            if self.getgoal==True:
                if self.on_main:
                    if self.main_back_mode==True:
                        if self.main_count!=0:
                            self.main_count-=1
                            return Agent.Action.FORWARD
                        else:
                            return Agent.Action.CLIMB
                    else:
                        if self.main_meet==False:
                            self.main_meet=True
                            return Agent.Action.TURN_LEFT
                        else:
                            self.main_back_mode=True
                            return Agent.Action.TURN_LEFT
                else:
                    if self.part_back_mode==True:
                        if self.part_count!=0:
                            self.part_count-=1
                            return Agent.Action.FORWARD
                        else:
                            self.on_main=True
                            return Agent.Action.TURN_LEFT
                    else:
                        if self.part_meet==False:
                            self.part_meet=True
                            return Agent.Action.TURN_LEFT
                        else:
                            self.part_back_mode=True
                            return Agent.Action.TURN_LEFT
            if self.main_meet==False:
                if (not stench and not breeze and not bump):
                    self.main_count+=1
                    return Agent.Action.FORWARD
                else:
                    if (breeze):
                        if (self.main_breeze):
                            pass
                        else:
                            self.main_breeze = True
                            self.main_meet = True
                            return Agent.Action.TURN_LEFT
                    elif (bump):
                        self.main_count -= 1
                        self.main_bump = True
                        self.main_meet = True
                        self.main_back_mode = True

                        self.on_main = False
                        self.on_part = True
                        self.part_back_mode = False
                        self.part_meet = False
                        self.part_count = 0
                        return Agent.Action.TURN_RIGHT
                    else:
                        if(self.monsteralive):
                                if (self.justshooted):
                                    self.justshooted = False
                                    self.main_count+=1
                                    return Agent.Action.FORWARD
                                else:
                                    if (self.shooted):
                                        self.main_meet = True
                                        return Agent.Action.TURN_LEFT
                                    else:
                                        self.shooted = True
                                        self.justshooted = True
                                        return Agent.Action.SHOOT
                        else:
                            self.main_count+=1
                            return Agent.Action.FORWARD



            if self.main_back_mode==False:
                self.main_back_mode = True
                return Agent.Action.TURN_LEFT
            
            if self.on_main==True:
                if self.main_count!=0:
                    if(self.main_breeze):
                        self.main_breeze = False
                        self.main_count -= 1
                        return Agent.Action.FORWARD
                    elif(stench):
                        if(self.monsteralive):
                            self.main_count -= 1
                            return Agent.Action.FORWARD
                        else:
                            self.on_main=False
                            self.on_part=True
                            self.part_back_mode=False
                            self.part_meet=False
                            self.part_count=0
                            return Agent.Action.TURN_LEFT
                    else:
                        self.on_main=False
                        self.on_part=True
                        self.part_back_mode=False
                        self.part_meet=False
                        self.part_count=0
                        return Agent.Action.TURN_LEFT
                else:
                    return Agent.Action.CLIMB

            if self.part_back_mode==False:
                if self.part_meet==False:
                    if (not stench and not breeze and not bump):
                       self.part_count += 1
                       return Agent.Action.FORWARD

                    else:
                        if (breeze):
                            self.part_meet = True
                            return Agent.Action.TURN_LEFT
                        elif(bump):
                            self.part_count -= 1
                            self.part_meet = True
                            return Agent.Action.TURN_LEFT
                        else:
                            if (self.monsteralive):
                                if (self.justshooted):
                                    self.justshooted = False
                                    self.part_count += 1
                                    return Agent.Action.FORWARD
                                else:
                                    if (self.shooted):
                                        self.part_meet = True
                                        return Agent.Action.TURN_LEFT
                                    else:
                                        self.shooted = True
                                        self.justshooted = True
                                        return Agent.Action.SHOOT
                            else:
                                self.part_count += 1
                                return Agent.Action.FORWARD
                else:
                    self.part_back_mode=True
                    return Agent.Action.TURN_LEFT
            else:
                if self.part_count!=0:
                    self.part_count-=1
                    return Agent.Action.FORWARD
                else:
                    if self.on_part==True:
                        self.on_part=False
                        return Agent.Action.TURN_LEFT
                    elif self.main_count!=0:
                        self.main_count-=1
                        self.on_main=True
                        return Agent.Action.FORWARD
                    else:
                        return Agent.Action.CLIMB





        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================
    
    # ======================================================================
    # YOUR CODE BEGINS
    # ======================================================================

    
    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================
