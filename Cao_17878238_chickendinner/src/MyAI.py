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
import queue
class MyAI ( Agent ):






    def __init__ ( self ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================

        self.current = (0, 0)
        self.NEXT = (0 , 0)
        self.stepCount  = 0 ;# count steps already been taken of AI
        self.arrow = 1;
        self.gold = 0;



        self.safe = set() ;
        self.safe_unvisited = set();
        self.visited = set() ;
        self.wumpus = set();
        self.pits = dict();

        self.wumpus_killed  = 0;

        self.actions = queue.Queue() ;  # when action buffer is not empty, excute action without check states
        self.direction = (1,0) ;  # 1.left 2.up 3.right 4.down
        self.X = float("inf") #Xbound
        self.Y = float("inf") #Ybound


        pass
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    def getAction( self, stench, breeze, glitter, bump, scream ):
        # ======================================================================
        # YOUR CODE BEGINS
        # =================================================== ===================
        # 0,none 1,breeze, 2.stench 3.glitter 4.scream 5.bump 6.breeze and stench


        cue = 0;

        if (glitter):
            self.gold = 1;
            return Agent.Action.GRAB;
        elif (bump):
            self.mark(5);
            if (self.direction[0] == 1 and self.direction[1] == 0):
                self.X = self.X - 1;
                self.NEXT = (self.current[0] - 2, self.current[1])
                self.actions.put(Agent.Action.TURN_LEFT)
                self.actions.put(Agent.Action.TURN_LEFT)
                self.actions.put(Agent.Action.FORWARD)
                self.current = (self.current[0] - self.direction[0], self.current[1] - self.direction[1])  # 定位修正


            elif (self.direction[0] == 0 and self.direction[1] == 1):
                self.Y = self.Y - 1;
                self.NEXT = (self.current[0], self.current[1] - 2)
                self.actions.put(Agent.Action.TURN_LEFT)
                self.actions.put(Agent.Action.TURN_LEFT)
                self.actions.put(Agent.Action.FORWARD)

                self.current = (self.current[0] - self.direction[0], self.current[1] - self.direction[1])  # 定位修正
        elif(breeze or stench or scream ):


            if(breeze and stench and scream):
                self.mark(6)
                pit = self.pits.keys()
                self.safe = self.safe.union(self.wumpus - pit) ;
                self.wumpus_killed = 1;


            elif(breeze and stench):
                self.mark(6);
                if (self.arrow):
                    self.actions.put(Agent.Action.SHOOT)
                    self.arrow = 0;


            elif(scream and stench):

                self.mark(0)
                self.safe = self.safe.union(self.wumpus)
                self.wumpus_killed = 1


            elif(breeze ):
                self.mark(1);
                if(self.current == (0,0)):  #原点感受到微风，直接回家
                    return Agent.Action.CLIMB;

            elif (stench):
                if(not self.wumpus_killed):
                    self.mark(2);
                    if (self.arrow):
                        self.actions.put(Agent.Action.SHOOT)
                        self.arrow = 0;
                else:

                    self.mark(0)








        else:
            self.mark(0);



        self.safe_unvisited  = self.safe - self.visited;



        if(self.current == self.NEXT ):
            self.NEXT = self.checkState(self.gold); # check state when reach next  position




        if(not self.actions.empty()):
            action = self.actions.get();




        if(action == Agent.Action.FORWARD ):
            self.current = (self.current[0]+self.direction[0],self.current[1]+self.direction[1])
        elif(action == Agent.Action.TURN_LEFT):
            if (self.direction[0] == 1 and self.direction[1] == 0):
                    self.direction = (0,1)
            elif (self.direction[0] == -1 and self.direction[1] == 0):
                    self.direction = (0,-1)
            elif (self.direction[0] == 0 and self.direction[1] == 1):
                    self.direction = (-1,0)
            elif (self.direction[0] == 0 and self.direction[1] == -1):
                    self.direction = (1,0)
        elif(action == Agent.Action.TURN_RIGHT):
            if (self.direction[0] == 1 and self.direction[1] == 0):
                    self.direction = (0,-1)
            elif (self.direction[0] == -1 and self.direction[1] == 0):
                    self.direction = (0,1)
            elif (self.direction[0] == 0 and self.direction[1] == 1):
                    self.direction = (1,0)
            elif (self.direction[0] == 0 and self.direction[1] == -1):
                    self.direction = (-1,0)



        return action
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================
    
    # ======================================================================
    # YOUR CODE BEGINS
    # ======================================================================


        # luochengxi's code



        # parameter, 2 tuples represent current and destination， return a safe shortest path including cur and dest.
    def dijkstra(self, source):
            Q = set(self.safe)

            dist = {}
            prev = {}
            drts = {}
            for each in Q:
                dist[each] = float('inf')
                prev[each] = None
                drts[each] = None
                dist[source] = 0
                drts[source] = tuple(self.direction)

            while len(Q) != 0:
                u = sorted(Q, key=lambda x: dist[x])[0]
                Q.remove(u)
                for v, drt in [((u[0] - 1, u[1]), (-1, 0)), ((u[0] + 1, u[1]), (1, 0)), ((u[0], u[1] + 1), (0, 1)),
                               ((u[0], u[1] - 1), (0, -1))]:
                    if v in self.safe:
                        alt = dist[u] + self.findCost(u, v, drts[u])
                        if alt < dist[v]:
                            dist[v] = alt
                            prev[v] = u
                            drts[v] = drt
            return prev

        # This method find the cost from current and next. Next is adjacent point of current.
    def findCost(self, current, next, cur_direction):
            cost = 0
            x = next[0] - current[0]
            y = next[1] - current[1]
            if (abs(x) == 1 and (y) == 0):  # current和next在一横排
                cost += 1
                if (abs(x - cur_direction[0]) == 2):  # 反方向掉头走
                    cost += 2;
                elif (abs(cur_direction[1] - y) == 1):  # 上下走
                    cost += 1;
            elif (abs(y) == 1 and (x) == 0):  # current和next在一竖列
                cost += 1
                if (abs(y - cur_direction[1]) == 2):  # 反方向掉头走
                    cost += 2;
                elif (abs(cur_direction[0] - x) == 1):  # 左右走
                    cost += 1;
            return cost

        # To get the list of path, call takeAction(dijkstra(start_node), start_node, end_node)
    def takeAction(self, prev, start, final):
            temp = [final]
            node = final
            while start not in temp:

                for key, value in prev.items():

                    if key == node:
                        temp.append(value)
                        node = value
            temp = temp[::-1]
            return temp

        # end of her code


    def checkState(self,gold=0):

        if(self.stepCount == 2):
            return

        if(len(self.safe_unvisited) == 0 or gold == 1):
            #do dijkstra and do actions

            

            path = self.takeAction(self.dijkstra(self.current), self.current, (0,0))
            self.path_to_actions(path)
            self.actions.put(Agent.Action.CLIMB);
            self.stepCount+=1;

            return (0,0)
            #回归到原点爬出去

        else:

            ac  = 0; #synchronize

            next = ()  # next destination
            minCost = float("inf");
            for p in self.safe_unvisited:
                cost = abs(p[0]-self.current[0]) + abs(p[1] - self.current[1]);
                if(p[0]-self.current[0] == self.direction[0] and p[1] - self.current[1] == self.direction[1] ):
                    cost += 0;
                else:
                    cost += 0.5;

                if(cost<minCost):
                    minCost = cost;
                    next = (p[0],p[1])

            #do dikjstra and do actions then update the current position
            path = self.takeAction(self.dijkstra(self.current), self.current, next)
            ac+=1
            action_counts = self.path_to_actions(path)



            return next

    def in_boundX(self,i):#标记点在X边界内
        if(i>=0 and i <=self.X):
            return 1;
        return 0;

    def in_boundY(self,i):#标记点在Y边界内
        if(i>=0 and i<=self.Y):
            return 1;
        return 0;

    def mark(self,sensor):
        self.visited.add(self.current); #添加当前位置到已访问集
        self.safe.add(self.current); #添加当前位置到安全集
        x = self.current[0]
        y = self.current[1]

        if (sensor == 5):
            clear = set();
            if (self.direction == (1, 0)):  # 向右碰壁，得到X最大边界
                self.X = x;
                for p in self.safe:
                    if (p[0] > self.X):
                        clear.add(p);  # 清除安全集中位于X边界外的点
                self.safe -= clear;
            elif (self.direction == (0, 1)):  # 向上碰壁，得到Y最大边界
                self.Y = y;
                for p in self.safe:
                    if (p[1] > self.Y):
                        clear.add(p);  # 清除安全集中位于Y边界外的点
                self.safe -= clear;


        ##标记上下左右4个坐标的信息
         #没有察觉到惨叫，就进行正常标记
        if(sensor!=4):
            self.mark_coordinate(x+1,y,sensor);
            self.mark_coordinate(x,y+1,sensor);
            self.mark_coordinate(x-1,y,sensor);
            self.mark_coordinate(x,y-1,sensor);


        ##标记结束
        return;


    #Path -> Action list
    def path_to_actions(self,paths):
        #decopose a position list to list of acions

        action_counts = 0;
        direct  = (self.direction[0],self.direction[1]) #模拟转向

        Acts = [
            Agent.Action.TURN_LEFT,
            Agent.Action.TURN_RIGHT,
            Agent.Action.FORWARD,
            Agent.Action.CLIMB,
            Agent.Action.SHOOT
        ]  # 0. left 1.right 2.forward 3. climb 4.shoot

        if(None in paths):
            paths.remove(None)
        current = paths[0]







        for i in range(1,len(paths)):
            next = paths[i];  #下一个需要抵达的地点


            d = (next[0] - current[0] ,next[1] - current[1]) #求方向差，需要移动的方向

            if(d[0] == direct[0]  and d[1] == direct[1]):
                self.actions.put(Acts[2])
                action_counts += 1;
            elif(direct[0] == 0 and direct[1] == 1):
                if(d[0] == 0 and d[1] == -1):
                    self.actions.put(Acts[1])
                    self.actions.put(Acts[1])
                    self.actions.put(Acts[2])
                    action_counts += 3;
                    direct = d
                    #Turn back and go
                elif (d[0] == 1 and d[1] == 0):
                    self.actions.put(Acts[1])
                    self.actions.put(Acts[2])
                    action_counts += 2;
                    direct = d
                    #Turn right and go
                elif (d[0] == -1 and d[1] == 0):
                    self.actions.put(Acts[0])
                    self.actions.put(Acts[2])
                    action_counts += 2;
                    direct = d
                    #Turn left and go
            elif (direct[0] == 0 and direct[1] == -1):
                if (d[0] == 0 and d[1] == 1):
                    self.actions.put(Acts[1])
                    self.actions.put(Acts[1])
                    self.actions.put(Acts[2])
                    action_counts += 3;
                    direct = d
                    # Turn back and go
                elif (d[0] == -1 and d[1] == 0):
                    self.actions.put(Acts[1])
                    self.actions.put(Acts[2])
                    action_counts += 2;
                    direct = d
                    #Turn right and go
                elif (d[0] == 1 and d[1] == 0):
                    self.actions.put(Acts[0])
                    self.actions.put(Acts[2])
                    action_counts += 2;
                    direct = d
                    #Turn left and go

            elif (direct[0] == 1 and direct[1] == 0):
                if (d[0] == -1 and d[1] == 0):
                    self.actions.put(Acts[1])
                    self.actions.put(Acts[1])
                    self.actions.put(Acts[2])
                    action_counts += 3;
                    direct = d
                    # Turn back and go
                elif (d[0] == 0 and d[1] == -1):
                    self.actions.put(Acts[1])
                    self.actions.put(Acts[2])
                    action_counts += 2;
                    direct = d
                    #Turn right and go
                elif (d[0] == 0 and d[1] == 1):
                    self.actions.put(Acts[0])
                    self.actions.put(Acts[2])
                    action_counts += 2;
                    direct = d
                    #Turn left and go

            elif (direct[0] == -1 and direct[1] == 0):
                if (d[0] == 1 and d[1] == 0):
                    self.actions.put(Acts[1])
                    self.actions.put(Acts[1])
                    self.actions.put(Acts[2])
                    action_counts += 3;
                    direct = d
                    # Turn back and go
                elif (d[0] == 0 and d[1] == 1):
                    self.actions.put(Acts[1])
                    self.actions.put(Acts[2])
                    action_counts += 2;
                    direct = d
                    #Turn right and go
                elif (d[0] == 0 and d[1] == -1):
                    self.actions.put(Acts[0])
                    self.actions.put(Acts[2])
                    action_counts += 2;
                    direct  = d
                    #Turn left and go


            current = next #更新当前位置
        return action_counts

    def mark_coordinate(self,x,y,sensor):
        if (self.in_boundX(x) and self.in_boundY(y) ):  # 确保标记点在地图范围以内
            if (sensor == 0):
                self.safe.add((x,y));
            elif(sensor == 1):
                if( (x,y) not in self.pits):
                    self.pits[(x,y)] = 0;
                else:
                    self.pits[(x,y)] +=1
            elif(sensor == 2 ):
                self.wumpus.add((x,y));

            elif(sensor == 4):
                # 杀死wumpus标记它的位置并，将wumpus集并入安全集
                self.safe  = self.safe.union(self.wumpus);
            elif(sensor == 6 ):
                if ((x, y) not in self.pits):
                    self.pits[(x, y)] = 0;
                else:
                    self.pits[(x, y)] += 1
                self.wumpus.add((x,y));








    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================

    def inference(self):


        return
