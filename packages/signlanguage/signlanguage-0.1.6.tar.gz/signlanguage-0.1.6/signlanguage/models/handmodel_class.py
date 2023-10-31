## hand modeltransform_zbody
class HandModel:
    ## calculate indertemidiate pairs points - handpoints diff  
    def make_model(self, hand_Left=None, hand_Right=None, points_body=None, face_relation=False, body_relation=False, hand_relation=False, hand_diff_relation=False):
        try:
            if hand_Left is None or hand_Right is None or points_body is None:
                return None

            ## hands difference --> when: hand_relation
            points_hand_diffX = [] #0
            points_hand_diffY = [] #1
            points_hand_diffZ = [] #2
            ## hands relation  --> indepent of hand_relation, same hands
            points_hand_Right_diffX = [] #3
            points_hand_Right_diffY = [] #4
            points_hand_Right_diffZ = [] #5
            points_hand_Left_diffX = [] #6
            points_hand_Left_diffY = [] #7
            points_hand_Left_diffZ  = [] #8
            ## hands relation  --> indepent of hand_relation, diff hands
            points_hand_relation_diffX = [] #9
            points_hand_relation_diffY = [] #10
            points_hand_relation_diffZ = [] #11
            ## body difference --> when: hand_relation
            points_body_diffX = [] #12
            points_body_diffY = [] #13
            points_body_diffZ = [] #14
            ## hands_body relation --> indepent of hand_relation, same hands
            points_body_XRight = [] #15
            points_body_YRight = [] #16
            points_body_ZRight = [] #17
            points_body_XLeft = [] #18
            points_body_YLeft = [] #19
            points_body_ZLeft = [] #20
            ## hands_body relation --> indepent of hand_relation, diff hands
            points_body_relation_diffXRight = [] #21
            points_body_relation_diffYRight = [] #22
            points_body_relation_diffZRight = [] #23
            points_body_relation_diffXLeft = [] #24
            points_body_relation_diffYLeft = [] #25
            points_body_relation_diffZLeft = [] #26
            ## body_face relation --> indepent of hand_relation, same hand
            points_body_face_XRight = [] #27
            points_body_face_YRight = [] #28
            points_body_face_ZRight = [] #29
            points_body_face_XLeft = []
            points_body_face_YLeft = []
            points_body_face_ZLeft = []
            ## body_face relation --> indepent of hand_relation, diff hand
            points_body_face_relation_diffXRight = []
            points_body_face_relation_diffYRight = []
            points_body_face_relation_diffZRight = []
            points_body_face_relation_diffXLeft = []
            points_body_face_relation_diffYLeft = []
            points_body_face_relation_diffZLeft = []
            ## face relation  --> indepent of hand_relation, sane hand
            points_face_XRight = []
            points_face_YRight = []
            points_face_ZRight = []
            points_face_XLeft = []
            points_face_YLeft = []
            points_face_ZLeft = []
            ## face relation  --> indepent of hand_relation, diff hand
            points_face_relation_diffXRight = []
            points_face_relation_diffYRight = []
            points_face_relation_diffZRight = []
            points_face_relation_diffXLeft = []
            points_face_relation_diffYLeft = []
            points_face_relation_diffZLeft = []

            #hands
            ## hands
            if len(hand_Right) > 0:
                hands_x = list(map(lambda a: (a['x']), hand_Right))
                hands_y = list(map(lambda a: (a['y']), hand_Right))
                hands_z = list(map(lambda a: (a['z']), hand_Right))
                
                points_hand_Right_diffX = [
                    #thumb
                    [(hands_x[4]-hands_x[3]),    4], [(hands_x[3]-hands_x[2]),    3], [(hands_x[2]-hands_x[1]),    2],
                    #index
                    [(hands_x[8]-hands_x[7]),    8], [(hands_x[7]-hands_x[6]),    7], [(hands_x[6]-hands_x[5]),    6],
                    #middle
                    [(hands_x[12]-hands_x[11]), 12], [(hands_x[11]-hands_x[10]), 11], [(hands_x[10]-hands_x[9]),  10],
                    #ring
                    [(hands_x[16]-hands_x[15]), 16], [(hands_x[15]-hands_x[14]), 15], [(hands_x[14]-hands_x[13]), 14],
                    #pinky
                    [(hands_x[20]-hands_x[19]), 20], [(hands_x[19]-hands_x[18]), 19], [(hands_x[18]-hands_x[17]), 18],
                    #to->wirst
                    [(hands_x[4]-hands_x[0]),    4], [(hands_x[8]-hands_x[0]),    8], [(hands_x[12]-hands_x[0]),  12],  [(hands_x[16]-hands_x[0]),  16],  [(hands_x[20]-hands_x[0]), 20],
                    #diff-between TIP
                    [(hands_x[4]-hands_x[8]),    4], [(hands_x[8]-hands_x[12]),   8], [(hands_x[12]-hands_x[16]), 12],  [(hands_x[16]-hands_x[20]), 16],  [(hands_x[16]-hands_x[4]), 16],
                    #diff-between IP
                    [(hands_x[3]-hands_x[7]),    3], [(hands_x[7]-hands_x[11]),   7], [(hands_x[11]-hands_x[15]), 11],  [(hands_x[15]-hands_x[19]), 15],  [(hands_x[19]-hands_x[3]), 19],
                    #diff-between MCP
                    [(hands_x[2]-hands_x[6]),    2], [(hands_x[6]-hands_x[10]),   6], [(hands_x[10]-hands_x[14]), 10],  [(hands_x[14]-hands_x[18]), 14],  [(hands_x[18]-hands_x[2]), 18],
                    #diff-between 
                    [(hands_x[4]-hands_x[6]),    4], [(hands_x[4]-hands_x[10]),   4], [(hands_x[4]-hands_x[14]),   4],  [(hands_x[4]-hands_x[18]),   4],
                    [(hands_x[8]-hands_x[2]),    8], [(hands_x[8]-hands_x[10]),   8], [(hands_x[8]-hands_x[14]),   8],  [(hands_x[8]-hands_x[18]),   8],
                    [(hands_x[12]-hands_x[2]),  12], [(hands_x[12]-hands_x[6]),  12], [(hands_x[12]-hands_x[14]), 12],  [(hands_x[12]-hands_x[18]), 12],
                    [(hands_x[16]-hands_x[2]),  16], [(hands_x[16]-hands_x[6]),  16], [(hands_x[16]-hands_x[10]), 16],  [(hands_x[16]-hands_x[18]), 16],
                    [(hands_x[20]-hands_x[2]),  20], [(hands_x[20]-hands_x[6]),  20], [(hands_x[20]-hands_x[10]), 20],  [(hands_x[20]-hands_x[14]), 20],
                    #diff-between 
                    [(hands_x[4]-hands_x[7]),    4], [(hands_x[4]-hands_x[11]),   4], [(hands_x[4]-hands_x[15]),   4],  [(hands_x[4]-hands_x[19]),   4],
                    [(hands_x[8]-hands_x[3]),    8], [(hands_x[8]-hands_x[11]),   8], [(hands_x[8]-hands_x[15]),   8],  [(hands_x[8]-hands_x[19]),   8],
                    [(hands_x[12]-hands_x[3]),  12], [(hands_x[12]-hands_x[7]),  12], [(hands_x[12]-hands_x[15]), 12],  [(hands_x[12]-hands_x[19]), 12],
                    [(hands_x[16]-hands_x[3]),  16], [(hands_x[16]-hands_x[7]),  16], [(hands_x[16]-hands_x[11]), 16],  [(hands_x[16]-hands_x[19]), 16],
                    [(hands_x[20]-hands_x[3]),  20], [(hands_x[20]-hands_x[7]),  20], [(hands_x[20]-hands_x[11]), 20],  [(hands_x[20]-hands_x[15]), 20],
                    #diff-between 
                    [(hands_x[4]-hands_x[8]),    4], [(hands_x[4]-hands_x[12]),   4], [(hands_x[4]-hands_x[16]),   4],  [(hands_x[4]-hands_x[20]),   4],
                    [(hands_x[8]-hands_x[4]),    8], [(hands_x[8]-hands_x[12]),   8], [(hands_x[8]-hands_x[16]),   8],  [(hands_x[8]-hands_x[20]),   8],
                    [(hands_x[12]-hands_x[4]),  12], [(hands_x[12]-hands_x[8]),  12], [(hands_x[12]-hands_x[16]), 12],  [(hands_x[12]-hands_x[20]), 12],
                    [(hands_x[16]-hands_x[4]),  16], [(hands_x[16]-hands_x[8]),  16], [(hands_x[16]-hands_x[12]), 16],  [(hands_x[16]-hands_x[20]), 16],
                    [(hands_x[20]-hands_x[4]),  20], [(hands_x[20]-hands_x[8]),  20], [(hands_x[20]-hands_x[12]), 20],  [(hands_x[20]-hands_x[16]), 20]
                ]
                
                points_hand_Right_diffY = [
                    [(hands_y[4]-hands_y[3]),    4], [(hands_y[3]-hands_y[2]),    3], [(hands_y[2]-hands_y[1]),    2],
                    [(hands_y[8]-hands_y[7]),    8], [(hands_y[7]-hands_y[6]),    7], [(hands_y[6]-hands_y[5]),    6],
                    [(hands_y[12]-hands_y[11]), 12], [(hands_y[11]-hands_y[10]), 11], [(hands_y[10]-hands_y[9]),  10],
                    [(hands_y[16]-hands_y[15]), 16], [(hands_y[15]-hands_y[14]), 15], [(hands_y[14]-hands_y[13]), 14],
                    [(hands_y[20]-hands_y[19]), 20], [(hands_y[19]-hands_y[18]), 19], [(hands_y[18]-hands_y[17]), 18],
                    #to->wirst
                    [(hands_y[4]-hands_y[0]),    4], [(hands_y[8]-hands_y[0]),    8], [(hands_y[12]-hands_y[0]),  12],  [(hands_y[16]-hands_y[0]),  16],  [(hands_y[20]-hands_y[0]), 20],
                    #diff-between TIP
                    [(hands_y[4]-hands_y[8]),    4], [(hands_y[8]-hands_y[12]),   8], [(hands_y[12]-hands_y[16]), 12],  [(hands_y[16]-hands_y[20]), 16],  [(hands_y[16]-hands_y[4]), 16],
                    #diff-between IP
                    [(hands_y[3]-hands_y[7]),    3], [(hands_y[7]-hands_y[11]),   7], [(hands_y[11]-hands_y[15]), 11],  [(hands_y[15]-hands_y[19]), 15],  [(hands_y[19]-hands_y[3]), 19],
                    #diff-between MCP
                    [(hands_y[2]-hands_y[6]),    2], [(hands_y[6]-hands_y[10]),   6], [(hands_y[10]-hands_y[14]), 10],  [(hands_y[14]-hands_y[18]), 14],  [(hands_y[18]-hands_y[2]), 18],
                    #diff-between 
                    [(hands_y[4]-hands_y[6]),    4], [(hands_y[4]-hands_y[10]),   4], [(hands_y[4]-hands_y[14]),   4],  [(hands_y[4]-hands_y[18]),   4],
                    [(hands_y[8]-hands_y[3]),    8], [(hands_y[8]-hands_y[10]),   8], [(hands_y[8]-hands_y[14]),   8],  [(hands_y[8]-hands_y[18]),   8],
                    [(hands_y[12]-hands_y[2]),  12], [(hands_y[12]-hands_y[6]),  12], [(hands_y[12]-hands_y[14]), 12],  [(hands_y[12]-hands_y[18]), 12],
                    [(hands_y[16]-hands_y[2]),  16], [(hands_y[16]-hands_y[6]),  16], [(hands_y[16]-hands_y[10]), 16],  [(hands_y[16]-hands_y[18]), 16],
                    [(hands_y[20]-hands_y[2]),  20], [(hands_y[20]-hands_y[6]),  20], [(hands_y[20]-hands_y[10]), 20],  [(hands_y[20]-hands_y[14]), 20],
                    #diff-between 
                    [(hands_y[4]-hands_y[7]),    4], [(hands_y[4]-hands_y[11]),   4], [(hands_y[4]-hands_y[15]),   4],  [(hands_y[4]-hands_y[19]),   4],
                    [(hands_y[8]-hands_y[3]),    8], [(hands_y[8]-hands_y[11]),   8], [(hands_y[8]-hands_y[15]),   8],  [(hands_y[8]-hands_y[19]),   8],
                    [(hands_y[12]-hands_y[3]),  12], [(hands_y[12]-hands_y[7]),  12], [(hands_y[12]-hands_y[15]), 12],  [(hands_y[12]-hands_y[19]), 12],
                    [(hands_y[16]-hands_y[3]),  16], [(hands_y[16]-hands_y[7]),  16], [(hands_y[16]-hands_y[11]), 16],  [(hands_y[16]-hands_y[19]), 16],
                    [(hands_y[20]-hands_y[3]),  20], [(hands_y[20]-hands_y[7]),  20], [(hands_y[20]-hands_y[11]), 20],  [(hands_y[20]-hands_y[15]), 20],
                    #diff-between 
                    [(hands_y[4]-hands_y[8]),    4], [(hands_y[4]-hands_y[12]),   4], [(hands_y[4]-hands_y[16]),   4],  [(hands_y[4]-hands_y[20]),   4],
                    [(hands_y[8]-hands_y[4]),    8], [(hands_y[8]-hands_y[12]),   8], [(hands_y[8]-hands_y[16]),   8],  [(hands_y[8]-hands_y[20]),   8],
                    [(hands_y[12]-hands_y[4]),  12], [(hands_y[12]-hands_y[8]),  12], [(hands_y[12]-hands_y[16]), 12],  [(hands_y[12]-hands_y[20]), 12],
                    [(hands_y[16]-hands_y[4]),  16], [(hands_y[16]-hands_y[8]),  16], [(hands_y[16]-hands_y[12]), 16],  [(hands_y[16]-hands_y[20]), 16],
                    [(hands_y[20]-hands_y[4]),  20], [(hands_y[20]-hands_y[8]),  20], [(hands_y[20]-hands_y[12]), 20],  [(hands_y[20]-hands_y[16]), 20]
                ]
                
                points_hand_Right_diffZ = [
                    [(hands_z[4]-hands_z[3]),    4], [(hands_z[3]-hands_z[2]),    3], [(hands_z[2]-hands_z[1]),    2],
                    [(hands_z[8]-hands_z[7]),    8], [(hands_z[7]-hands_z[6]),    7], [(hands_z[6]-hands_z[5]),    6],
                    [(hands_z[12]-hands_z[11]), 12], [(hands_z[11]-hands_z[10]), 11], [(hands_z[10]-hands_z[9]),  10],
                    [(hands_z[16]-hands_z[15]), 16], [(hands_z[15]-hands_z[14]), 15], [(hands_z[14]-hands_z[13]), 14],
                    [(hands_z[20]-hands_z[19]), 20], [(hands_z[19]-hands_z[18]), 19], [(hands_z[18]-hands_z[17]), 18],
                    #to->wirst
                    [(hands_z[4]-hands_z[0]),    4], [(hands_z[8]-hands_z[0]),    8], [(hands_z[12]-hands_z[0]),  12],  [(hands_z[16]-hands_z[0]),  16],  [(hands_z[20]-hands_z[0]), 20],
                    #diff-between TIP
                    [(hands_z[4]-hands_z[8]),    4], [(hands_z[8]-hands_z[12]),   8], [(hands_z[12]-hands_z[16]), 12],  [(hands_z[16]-hands_z[20]), 16],  [(hands_z[16]-hands_z[4]), 16],
                    #diff-between IP
                    [(hands_z[3]-hands_z[7]),    3], [(hands_z[7]-hands_z[11]),   7], [(hands_z[11]-hands_z[15]), 11],  [(hands_z[15]-hands_z[19]), 15],  [(hands_z[19]-hands_z[3]), 19],
                    #diff-between MCP
                    [(hands_z[2]-hands_z[6]),    2], [(hands_z[6]-hands_z[10]),   6], [(hands_z[10]-hands_z[14]), 10],  [(hands_z[14]-hands_z[18]), 14],  [(hands_z[18]-hands_z[2]), 18],
                    #diff-between 
                    [(hands_z[4]-hands_z[6]),    4], [(hands_z[4]-hands_z[10]),   4], [(hands_z[4]-hands_z[14]),   4],  [(hands_z[4]-hands_z[18]),   4],
                    [(hands_z[8]-hands_z[3]),    8], [(hands_z[8]-hands_z[10]),   8], [(hands_z[8]-hands_z[14]),   8],  [(hands_z[8]-hands_z[18]),   8],
                    [(hands_z[12]-hands_z[2]),  12], [(hands_z[12]-hands_z[6]),  12], [(hands_z[12]-hands_z[14]), 12],  [(hands_z[12]-hands_z[18]), 12],
                    [(hands_z[16]-hands_z[2]),  16], [(hands_z[16]-hands_z[6]),  16], [(hands_z[16]-hands_z[10]), 16],  [(hands_z[16]-hands_z[18]), 16],
                    [(hands_z[20]-hands_z[2]),  20], [(hands_z[20]-hands_z[6]),  20], [(hands_z[20]-hands_z[10]), 20],  [(hands_z[20]-hands_z[14]), 20],
                    #diff-between 
                    [(hands_z[4]-hands_z[7]),    4], [(hands_z[4]-hands_z[11]),   4], [(hands_z[4]-hands_z[15]),   4],  [(hands_z[4]-hands_z[19]),   4],
                    [(hands_z[8]-hands_z[3]),    8], [(hands_z[8]-hands_z[11]),   8], [(hands_z[8]-hands_z[15]),   8],  [(hands_z[8]-hands_z[19]),   8],
                    [(hands_z[12]-hands_z[3]),  12], [(hands_z[12]-hands_z[7]),  12], [(hands_z[12]-hands_z[15]), 12],  [(hands_z[12]-hands_z[19]), 12],
                    [(hands_z[16]-hands_z[3]),  16], [(hands_z[16]-hands_z[7]),  16], [(hands_z[16]-hands_z[11]), 16],  [(hands_z[16]-hands_z[19]), 16],
                    [(hands_z[20]-hands_z[3]),  20], [(hands_z[20]-hands_z[7]),  20], [(hands_z[20]-hands_z[11]), 20],  [(hands_z[20]-hands_z[15]), 20],
                    #diff-between 
                    [(hands_z[4]-hands_z[8]),    4], [(hands_z[4]-hands_z[12]),   4], [(hands_z[4]-hands_z[16]),   4],  [(hands_z[4]-hands_z[20]),   4],
                    [(hands_z[8]-hands_z[4]),    8], [(hands_z[8]-hands_z[12]),   8], [(hands_z[8]-hands_z[16]),   8],  [(hands_z[8]-hands_z[20]),   8],
                    [(hands_z[12]-hands_z[4]),  12], [(hands_z[12]-hands_z[8]),  12], [(hands_z[12]-hands_z[16]), 12],  [(hands_z[12]-hands_z[20]), 12],
                    [(hands_z[16]-hands_z[4]),  16], [(hands_z[16]-hands_z[8]),  16], [(hands_z[16]-hands_z[12]), 16],  [(hands_z[16]-hands_z[20]), 16],
                    [(hands_z[20]-hands_z[4]),  20], [(hands_z[20]-hands_z[8]),  20], [(hands_z[20]-hands_z[12]), 20],  [(hands_z[20]-hands_z[16]), 20]
                ]

            if len(hand_Left) > 0:

                hands_x = list(map(lambda a: (a['x']), hand_Left))
                hands_y = list(map(lambda a: (a['y']), hand_Left))
                hands_z = list(map(lambda a: (a['z']), hand_Left))

                points_hand_Left_diffX= [
                    [(hands_x[4]-hands_x[3]),    4], [(hands_x[3]-hands_x[2]),    3], [(hands_x[2]-hands_x[1]),    2],
                    [(hands_x[8]-hands_x[7]),    8], [(hands_x[7]-hands_x[6]),    7], [(hands_x[6]-hands_x[5]),    6],
                    [(hands_x[12]-hands_x[11]), 12], [(hands_x[11]-hands_x[10]), 11], [(hands_x[10]-hands_x[9]),  10],
                    [(hands_x[16]-hands_x[15]), 16], [(hands_x[15]-hands_x[14]), 15], [(hands_x[14]-hands_x[13]), 14],
                    [(hands_x[20]-hands_x[19]), 20], [(hands_x[19]-hands_x[18]), 19], [(hands_x[18]-hands_x[17]), 18],
                    #to->wirst
                    [(hands_x[4]-hands_x[0]),    4], [(hands_x[8]-hands_x[0]),    8], [(hands_x[12]-hands_x[0]),  12],  [(hands_x[16]-hands_x[0]),  16],  [(hands_x[20]-hands_x[0]), 20],
                    #diff-between TIP
                    [(hands_x[4]-hands_x[8]),    4], [(hands_x[8]-hands_x[12]),   8], [(hands_x[12]-hands_x[16]), 12],  [(hands_x[16]-hands_x[20]), 16],  [(hands_x[16]-hands_x[4]), 16],
                    #diff-between IP
                    [(hands_x[3]-hands_x[7]),    3], [(hands_x[7]-hands_x[11]),   7], [(hands_x[11]-hands_x[15]), 11],  [(hands_x[15]-hands_x[19]), 15],  [(hands_x[19]-hands_x[3]), 19],
                    #diff-between MCP
                    [(hands_x[2]-hands_x[6]),    2], [(hands_x[6]-hands_x[10]),   6], [(hands_x[10]-hands_x[14]), 10],  [(hands_x[14]-hands_x[18]), 14],  [(hands_x[18]-hands_x[2]), 18],
                    #diff-between MCP
                    [(hands_x[4]-hands_x[6]),    4], [(hands_x[4]-hands_x[10]),   4], [(hands_x[4]-hands_x[14]),   4],  [(hands_x[4]-hands_x[18]),   4],
                    [(hands_x[8]-hands_x[3]),    8], [(hands_x[8]-hands_x[10]),   8], [(hands_x[8]-hands_x[14]),   8],  [(hands_x[8]-hands_x[18]),   8],
                    [(hands_x[12]-hands_x[2]),  12], [(hands_x[12]-hands_x[6]),  12], [(hands_x[12]-hands_x[14]), 12],  [(hands_x[12]-hands_x[18]), 12],
                    [(hands_x[16]-hands_x[2]),  16], [(hands_x[16]-hands_x[6]),  16], [(hands_x[16]-hands_x[10]), 16],  [(hands_x[16]-hands_x[18]), 16],
                    [(hands_x[20]-hands_x[2]),  20], [(hands_x[20]-hands_x[6]),  20], [(hands_x[20]-hands_x[10]), 20],  [(hands_x[20]-hands_x[14]), 20],
                    #diff-between IP
                    [(hands_x[4]-hands_x[7]),    4], [(hands_x[4]-hands_x[11]),   4], [(hands_x[4]-hands_x[15]),   4],  [(hands_x[4]-hands_x[19]),   4],
                    [(hands_x[8]-hands_x[3]),    8], [(hands_x[8]-hands_x[11]),   8], [(hands_x[8]-hands_x[15]),   8],  [(hands_x[8]-hands_x[19]),   8],
                    [(hands_x[12]-hands_x[3]),  12], [(hands_x[12]-hands_x[7]),  12], [(hands_x[12]-hands_x[15]), 12],  [(hands_x[12]-hands_x[19]), 12],
                    [(hands_x[16]-hands_x[3]),  16], [(hands_x[16]-hands_x[7]),  16], [(hands_x[16]-hands_x[11]), 16],  [(hands_x[16]-hands_x[19]), 16],
                    [(hands_x[20]-hands_x[3]),  20], [(hands_x[20]-hands_x[7]),  20], [(hands_x[20]-hands_x[11]), 20],  [(hands_x[20]-hands_x[15]), 20],
                    #diff-between 
                    [(hands_x[4]-hands_x[8]),    4], [(hands_x[4]-hands_x[12]),   4], [(hands_x[4]-hands_x[16]),   4],  [(hands_x[4]-hands_x[20]),   4],
                    [(hands_x[8]-hands_x[4]),    8], [(hands_x[8]-hands_x[12]),   8], [(hands_x[8]-hands_x[16]),   8],  [(hands_x[8]-hands_x[20]),   8],
                    [(hands_x[12]-hands_x[4]),  12], [(hands_x[12]-hands_x[8]),  12], [(hands_x[12]-hands_x[16]), 12],  [(hands_x[12]-hands_x[20]), 12],
                    [(hands_x[16]-hands_x[4]),  16], [(hands_x[16]-hands_x[8]),  16], [(hands_x[16]-hands_x[12]), 16],  [(hands_x[16]-hands_x[20]), 16],
                    [(hands_x[20]-hands_x[4]),  20], [(hands_x[20]-hands_x[8]),  20], [(hands_x[20]-hands_x[12]), 20],  [(hands_x[20]-hands_x[16]), 20]
                    
                ]

                points_hand_Left_diffY = [
                    [(hands_y[4]-hands_y[3]),    4], [(hands_y[3]-hands_y[2]),    3], [(hands_y[2]-hands_y[1]),    2],
                    [(hands_y[8]-hands_y[7]),    8], [(hands_y[7]-hands_y[6]),    7], [(hands_y[6]-hands_y[5]),    6],
                    [(hands_y[12]-hands_y[11]), 12], [(hands_y[11]-hands_y[10]), 11], [(hands_y[10]-hands_y[9]),  10],
                    [(hands_y[16]-hands_y[15]), 16], [(hands_y[15]-hands_y[14]), 15], [(hands_y[14]-hands_y[13]), 14],
                    [(hands_y[20]-hands_y[19]), 20], [(hands_y[19]-hands_y[18]), 19], [(hands_y[18]-hands_y[17]), 18],
                    #to->wirst
                    [(hands_y[4]-hands_y[0]),    4], [(hands_y[8]-hands_y[0]),    8], [(hands_y[12]-hands_y[0]),  12],  [(hands_y[16]-hands_y[0]),  16],  [(hands_y[20]-hands_y[0]), 20],
                    #diff-between TIP
                    [(hands_y[4]-hands_y[8]),    4], [(hands_y[8]-hands_y[12]),   8], [(hands_y[12]-hands_y[16]), 12],  [(hands_y[16]-hands_y[20]), 16],  [(hands_y[16]-hands_y[4]), 16],
                    #diff-between IP
                    [(hands_y[3]-hands_y[7]),    3], [(hands_y[7]-hands_y[11]),   7], [(hands_y[11]-hands_y[15]), 11],  [(hands_y[15]-hands_y[19]), 15],  [(hands_y[19]-hands_y[3]), 19],
                    #diff-between MCP
                    [(hands_y[2]-hands_y[6]),    2], [(hands_y[6]-hands_y[10]),   6], [(hands_y[10]-hands_y[14]), 10],  [(hands_y[14]-hands_y[18]), 14],  [(hands_y[18]-hands_y[2]), 18],
                    #diff-between 
                    [(hands_y[4]-hands_y[6]),    4], [(hands_y[4]-hands_y[10]),   4], [(hands_y[4]-hands_y[14]),   4],  [(hands_y[4]-hands_y[18]),   4],
                    [(hands_y[8]-hands_y[3]),    8], [(hands_y[8]-hands_y[10]),   8], [(hands_y[8]-hands_y[14]),   8],  [(hands_y[8]-hands_y[18]),   8],
                    [(hands_y[12]-hands_y[2]),  12], [(hands_y[12]-hands_y[6]),  12], [(hands_y[12]-hands_y[14]), 12],  [(hands_y[12]-hands_y[18]), 12],
                    [(hands_y[16]-hands_y[2]),  16], [(hands_y[16]-hands_y[6]),  16], [(hands_y[16]-hands_y[10]), 16],  [(hands_y[16]-hands_y[18]), 16],
                    [(hands_y[20]-hands_y[2]),  20], [(hands_y[20]-hands_y[6]),  20], [(hands_y[20]-hands_y[10]), 20],  [(hands_y[20]-hands_y[14]), 20],
                    #diff-between 
                    [(hands_y[4]-hands_y[7]),    4], [(hands_y[4]-hands_y[11]),   4], [(hands_y[4]-hands_y[15]),   4],  [(hands_y[4]-hands_y[19]),   4],
                    [(hands_y[8]-hands_y[3]),    8], [(hands_y[8]-hands_y[11]),   8], [(hands_y[8]-hands_y[15]),   8],  [(hands_y[8]-hands_y[19]),   8],
                    [(hands_y[12]-hands_y[3]),  12], [(hands_y[12]-hands_y[7]),  12], [(hands_y[12]-hands_y[15]), 12],  [(hands_y[12]-hands_y[19]), 12],
                    [(hands_y[16]-hands_y[3]),  16], [(hands_y[16]-hands_y[7]),  16], [(hands_y[16]-hands_y[11]), 16],  [(hands_y[16]-hands_y[19]), 16],
                    [(hands_y[20]-hands_y[3]),  20], [(hands_y[20]-hands_y[7]),  20], [(hands_y[20]-hands_y[11]), 20],  [(hands_y[20]-hands_y[15]), 20],
                    #diff-between 
                    [(hands_y[4]-hands_y[8]),    4], [(hands_y[4]-hands_y[12]),   4], [(hands_y[4]-hands_y[16]),   4],  [(hands_y[4]-hands_y[20]),   4],
                    [(hands_y[8]-hands_y[4]),    8], [(hands_y[8]-hands_y[12]),   8], [(hands_y[8]-hands_y[16]),   8],  [(hands_y[8]-hands_y[20]),   8],
                    [(hands_y[12]-hands_y[4]),  12], [(hands_y[12]-hands_y[8]),  12], [(hands_y[12]-hands_y[16]), 12],  [(hands_y[12]-hands_y[20]), 12],
                    [(hands_y[16]-hands_y[4]),  16], [(hands_y[16]-hands_y[8]),  16], [(hands_y[16]-hands_y[12]), 16],  [(hands_y[16]-hands_y[20]), 16],
                    [(hands_y[20]-hands_y[4]),  20], [(hands_y[20]-hands_y[8]),  20], [(hands_y[20]-hands_y[12]), 20],  [(hands_y[20]-hands_y[16]), 20]
                ]

                points_hand_Left_diffZ = [
                    [(hands_z[4]-hands_z[3]),    4], [(hands_z[3]-hands_z[2]),    3], [(hands_z[2]-hands_z[1]),    2],
                    [(hands_z[8]-hands_z[7]),    8], [(hands_z[7]-hands_z[6]),    7], [(hands_z[6]-hands_z[5]),    6],
                    [(hands_z[12]-hands_z[11]), 12], [(hands_z[11]-hands_z[10]), 11], [(hands_z[10]-hands_z[9]),  10],
                    [(hands_z[16]-hands_z[15]), 16], [(hands_z[15]-hands_z[14]), 15], [(hands_z[14]-hands_z[13]), 14],
                    [(hands_z[20]-hands_z[19]), 20], [(hands_z[19]-hands_z[18]), 19], [(hands_z[18]-hands_z[17]), 18],
                    #to->wirst
                    [(hands_z[4]-hands_z[0]),    4], [(hands_z[8]-hands_z[0]),    8], [(hands_z[12]-hands_z[0]),  12],  [(hands_z[16]-hands_z[0]),  16],  [(hands_z[20]-hands_z[0]), 20],
                    #diff-between TIP
                    [(hands_z[4]-hands_z[8]),    4], [(hands_z[8]-hands_z[12]),   8], [(hands_z[12]-hands_z[16]), 12],  [(hands_z[16]-hands_z[20]), 16],  [(hands_z[16]-hands_z[4]), 16],
                    #diff-between IP
                    [(hands_z[3]-hands_z[7]),    3], [(hands_z[7]-hands_z[11]),   7], [(hands_z[11]-hands_z[15]), 11],  [(hands_z[15]-hands_z[19]), 15],  [(hands_z[19]-hands_z[3]), 19],
                    #diff-between MCP
                    [(hands_z[2]-hands_z[6]),    2], [(hands_z[6]-hands_z[10]),   6], [(hands_z[10]-hands_z[14]), 10],  [(hands_z[14]-hands_z[18]), 14],  [(hands_z[18]-hands_z[2]), 18],
                    #diff-between 
                    [(hands_z[4]-hands_z[6]),    4], [(hands_z[4]-hands_z[10]),   4], [(hands_z[4]-hands_z[14]),   4],  [(hands_z[4]-hands_z[18]),   4],
                    [(hands_z[8]-hands_z[3]),    8], [(hands_z[8]-hands_z[10]),   8], [(hands_z[8]-hands_z[14]),   8],  [(hands_z[8]-hands_z[18]),   8],
                    [(hands_z[12]-hands_z[2]),  12], [(hands_z[12]-hands_z[6]),  12], [(hands_z[12]-hands_z[14]), 12],  [(hands_z[12]-hands_z[18]), 12],
                    [(hands_z[16]-hands_z[2]),  16], [(hands_z[16]-hands_z[6]),  16], [(hands_z[16]-hands_z[10]), 16],  [(hands_z[16]-hands_z[18]), 16],
                    [(hands_z[20]-hands_z[2]),  20], [(hands_z[20]-hands_z[6]),  20], [(hands_z[20]-hands_z[10]), 20],  [(hands_z[20]-hands_z[14]), 20],
                    #diff-between 
                    [(hands_z[4]-hands_z[7]),    4], [(hands_z[4]-hands_z[11]),   4], [(hands_z[4]-hands_z[15]),   4],  [(hands_z[4]-hands_z[19]),   4],
                    [(hands_z[8]-hands_z[3]),    8], [(hands_z[8]-hands_z[11]),   8], [(hands_z[8]-hands_z[15]),   8],  [(hands_z[8]-hands_z[19]),   8],
                    [(hands_z[12]-hands_z[3]),  12], [(hands_z[12]-hands_z[7]),  12], [(hands_z[12]-hands_z[15]), 12],  [(hands_z[12]-hands_z[19]), 12],
                    [(hands_z[16]-hands_z[3]),  16], [(hands_z[16]-hands_z[7]),  16], [(hands_z[16]-hands_z[11]), 16],  [(hands_z[16]-hands_z[19]), 16],
                    [(hands_z[20]-hands_z[3]),  20], [(hands_z[20]-hands_z[7]),  20], [(hands_z[20]-hands_z[11]), 20],  [(hands_z[20]-hands_z[15]), 20],
                    #diff-between 
                    [(hands_z[4]-hands_z[8]),    4], [(hands_z[4]-hands_z[12]),   4], [(hands_z[4]-hands_z[16]),   4],  [(hands_z[4]-hands_z[20]),   4],
                    [(hands_z[8]-hands_z[4]),    8], [(hands_z[8]-hands_z[12]),   8], [(hands_z[8]-hands_z[16]),   8],  [(hands_z[8]-hands_z[20]),   8],
                    [(hands_z[12]-hands_z[4]),  12], [(hands_z[12]-hands_z[8]),  12], [(hands_z[12]-hands_z[16]), 12],  [(hands_z[12]-hands_z[20]), 12],
                    [(hands_z[16]-hands_z[4]),  16], [(hands_z[16]-hands_z[8]),  16], [(hands_z[16]-hands_z[12]), 16],  [(hands_z[16]-hands_z[20]), 16],
                    [(hands_z[20]-hands_z[4]),  20], [(hands_z[20]-hands_z[8]),  20], [(hands_z[20]-hands_z[12]), 20],  [(hands_z[20]-hands_z[16]), 20]
                ]
                
            if len(hand_Right) > 0 and len(hand_Left) > 0 and hand_diff_relation:

                ### hand Right
                hands_x1 = list(map(lambda a: (a['x']), hand_Right))
                hands_y1 = list(map(lambda a: (a['y']), hand_Right))
                hands_z1 = list(map(lambda a: (a['z']), hand_Right))
                ### hand Left
                hands_x2 = list(map(lambda a: (a['x']), hand_Left))
                hands_y2 = list(map(lambda a: (a['y']), hand_Left))
                hands_z2 = list(map(lambda a: (a['z']), hand_Left))
                
                points_hand_relation_diffX = [
                    #thumb
                    [(hands_x1[4]-hands_x2[0]),    4], [(hands_x1[3]-hands_x2[0]),    3], [(hands_x1[2]-hands_x2[0]),    2], [(hands_x1[1]-hands_x2[0]),    1],
                    [(hands_x1[4]-hands_x2[1]),    4], [(hands_x1[3]-hands_x2[1]),    3], [(hands_x1[2]-hands_x2[1]),    2], [(hands_x1[1]-hands_x2[1]),    1],
                    [(hands_x1[4]-hands_x2[2]),    4], [(hands_x1[3]-hands_x2[2]),    3], [(hands_x1[2]-hands_x2[2]),    2], [(hands_x1[1]-hands_x2[2]),    1],
                    [(hands_x1[4]-hands_x2[3]),    4], [(hands_x1[3]-hands_x2[3]),    3], [(hands_x1[2]-hands_x2[3]),    2], [(hands_x1[1]-hands_x2[3]),    1],
                    [(hands_x1[4]-hands_x2[4]),    4], [(hands_x1[3]-hands_x2[4]),    3], [(hands_x1[2]-hands_x2[4]),    2], [(hands_x1[1]-hands_x2[4]),    1],
                    [(hands_x1[4]-hands_x2[6]),    4], [(hands_x1[3]-hands_x2[5]),    3], [(hands_x1[2]-hands_x2[5]),    2], [(hands_x1[1]-hands_x2[5]),    1],
                    [(hands_x1[4]-hands_x2[6]),    4], [(hands_x1[3]-hands_x2[6]),    3], [(hands_x1[2]-hands_x2[6]),    2], [(hands_x1[1]-hands_x2[6]),    1],
                    [(hands_x1[4]-hands_x2[7]),    4], [(hands_x1[3]-hands_x2[7]),    3], [(hands_x1[2]-hands_x2[7]),    2], [(hands_x1[1]-hands_x2[7]),    1],
                    [(hands_x1[4]-hands_x2[8]),    4], [(hands_x1[3]-hands_x2[8]),    3], [(hands_x1[2]-hands_x2[8]),    2], [(hands_x1[1]-hands_x2[8]),    1],
                    [(hands_x1[4]-hands_x2[9]),    4], [(hands_x1[3]-hands_x2[9]),    3], [(hands_x1[2]-hands_x2[9]),    2], [(hands_x1[1]-hands_x2[9]),    1],
                    [(hands_x1[4]-hands_x2[10]),   4], [(hands_x1[3]-hands_x2[10]),   3], [(hands_x1[2]-hands_x2[10]),   2], [(hands_x1[1]-hands_x2[10]),   1],
                    [(hands_x1[4]-hands_x2[11]),   4], [(hands_x1[3]-hands_x2[11]),   3], [(hands_x1[2]-hands_x2[11]),   2], [(hands_x1[1]-hands_x2[11]),   1],
                    [(hands_x1[4]-hands_x2[12]),   4], [(hands_x1[3]-hands_x2[12]),   3], [(hands_x1[2]-hands_x2[12]),   2], [(hands_x1[1]-hands_x2[12]),   1],
                    [(hands_x1[4]-hands_x2[13]),   4], [(hands_x1[3]-hands_x2[13]),   3], [(hands_x1[2]-hands_x2[13]),   2], [(hands_x1[1]-hands_x2[13]),   1],
                    [(hands_x1[4]-hands_x2[14]),   4], [(hands_x1[3]-hands_x2[14]),   3], [(hands_x1[2]-hands_x2[14]),   2], [(hands_x1[1]-hands_x2[14]),   1],
                    [(hands_x1[4]-hands_x2[15]),   4], [(hands_x1[3]-hands_x2[15]),   3], [(hands_x1[2]-hands_x2[15]),   2], [(hands_x1[1]-hands_x2[15]),   1],
                    [(hands_x1[4]-hands_x2[16]),   4], [(hands_x1[3]-hands_x2[16]),   3], [(hands_x1[2]-hands_x2[16]),   2], [(hands_x1[1]-hands_x2[16]),   1],
                    [(hands_x1[4]-hands_x2[17]),   4], [(hands_x1[3]-hands_x2[17]),   3], [(hands_x1[2]-hands_x2[17]),   2], [(hands_x1[1]-hands_x2[17]),   1],
                    [(hands_x1[4]-hands_x2[18]),   4], [(hands_x1[3]-hands_x2[18]),   3], [(hands_x1[2]-hands_x2[18]),   2], [(hands_x1[1]-hands_x2[18]),   1],
                    [(hands_x1[4]-hands_x2[19]),   4], [(hands_x1[3]-hands_x2[19]),   3], [(hands_x1[2]-hands_x2[19]),   2], [(hands_x1[1]-hands_x2[19]),   1],
                    [(hands_x1[4]-hands_x2[20]),   4], [(hands_x1[3]-hands_x2[20]),   3], [(hands_x1[2]-hands_x2[20]),   2], [(hands_x1[1]-hands_x2[20]),   1],
                    #index
                    [(hands_x1[8]-hands_x2[0]),    8], [(hands_x1[7]-hands_x2[0]),    7], [(hands_x1[6]-hands_x2[0]),    6], [(hands_x1[5]-hands_x2[0]),    5],
                    [(hands_x1[8]-hands_x2[1]),    8], [(hands_x1[7]-hands_x2[1]),    7], [(hands_x1[6]-hands_x2[1]),    6], [(hands_x1[5]-hands_x2[1]),    5],
                    [(hands_x1[8]-hands_x2[2]),    8], [(hands_x1[7]-hands_x2[2]),    7], [(hands_x1[6]-hands_x2[2]),    6], [(hands_x1[5]-hands_x2[2]),    5],
                    [(hands_x1[8]-hands_x2[3]),    8], [(hands_x1[7]-hands_x2[3]),    7], [(hands_x1[6]-hands_x2[3]),    6], [(hands_x1[5]-hands_x2[3]),    5],
                    [(hands_x1[8]-hands_x2[4]),    8], [(hands_x1[7]-hands_x2[4]),    7], [(hands_x1[6]-hands_x2[4]),    6], [(hands_x1[5]-hands_x2[4]),    5],
                    [(hands_x1[8]-hands_x2[6]),    8], [(hands_x1[7]-hands_x2[5]),    7], [(hands_x1[6]-hands_x2[5]),    6], [(hands_x1[5]-hands_x2[5]),    5],
                    [(hands_x1[8]-hands_x2[6]),    8], [(hands_x1[7]-hands_x2[6]),    7], [(hands_x1[6]-hands_x2[6]),    6], [(hands_x1[5]-hands_x2[6]),    5],
                    [(hands_x1[8]-hands_x2[7]),    8], [(hands_x1[7]-hands_x2[7]),    7], [(hands_x1[6]-hands_x2[7]),    6], [(hands_x1[5]-hands_x2[7]),    5],
                    [(hands_x1[8]-hands_x2[8]),    8], [(hands_x1[7]-hands_x2[8]),    7], [(hands_x1[6]-hands_x2[8]),    6], [(hands_x1[5]-hands_x2[8]),    5],
                    [(hands_x1[8]-hands_x2[9]),    8], [(hands_x1[7]-hands_x2[9]),    7], [(hands_x1[6]-hands_x2[9]),    6], [(hands_x1[5]-hands_x2[9]),    5],
                    [(hands_x1[8]-hands_x2[10]),   8], [(hands_x1[7]-hands_x2[10]),   7], [(hands_x1[6]-hands_x2[10]),   6], [(hands_x1[5]-hands_x2[10]),   5],
                    [(hands_x1[8]-hands_x2[11]),   8], [(hands_x1[7]-hands_x2[11]),   7], [(hands_x1[6]-hands_x2[11]),   6], [(hands_x1[5]-hands_x2[11]),   5],
                    [(hands_x1[8]-hands_x2[12]),   8], [(hands_x1[7]-hands_x2[12]),   7], [(hands_x1[6]-hands_x2[12]),   6], [(hands_x1[5]-hands_x2[12]),   5],
                    [(hands_x1[8]-hands_x2[13]),   8], [(hands_x1[7]-hands_x2[13]),   7], [(hands_x1[6]-hands_x2[13]),   6], [(hands_x1[5]-hands_x2[13]),   5],
                    [(hands_x1[8]-hands_x2[14]),   8], [(hands_x1[7]-hands_x2[14]),   7], [(hands_x1[6]-hands_x2[14]),   6], [(hands_x1[5]-hands_x2[14]),   5],
                    [(hands_x1[8]-hands_x2[15]),   8], [(hands_x1[7]-hands_x2[15]),   7], [(hands_x1[6]-hands_x2[15]),   6], [(hands_x1[5]-hands_x2[15]),   5],
                    [(hands_x1[8]-hands_x2[16]),   8], [(hands_x1[7]-hands_x2[16]),   7], [(hands_x1[6]-hands_x2[16]),   6], [(hands_x1[5]-hands_x2[16]),   5],
                    [(hands_x1[8]-hands_x2[17]),   8], [(hands_x1[7]-hands_x2[17]),   7], [(hands_x1[6]-hands_x2[17]),   6], [(hands_x1[5]-hands_x2[17]),   5],
                    [(hands_x1[8]-hands_x2[18]),   8], [(hands_x1[7]-hands_x2[18]),   7], [(hands_x1[6]-hands_x2[18]),   6], [(hands_x1[5]-hands_x2[18]),   5],
                    [(hands_x1[8]-hands_x2[19]),   8], [(hands_x1[7]-hands_x2[19]),   7], [(hands_x1[6]-hands_x2[19]),   6], [(hands_x1[5]-hands_x2[19]),   5],
                    [(hands_x1[8]-hands_x2[20]),   8], [(hands_x1[7]-hands_x2[20]),   7], [(hands_x1[6]-hands_x2[20]),   6], [(hands_x1[5]-hands_x2[20]),   5],
                    #middle
                    [(hands_x1[12]-hands_x2[0]),  12], [(hands_x1[11]-hands_x2[0]),  11], [(hands_x1[10]-hands_x2[0]),  10], [(hands_x1[9]-hands_x2[0]),    9],
                    [(hands_x1[12]-hands_x2[1]),  12], [(hands_x1[11]-hands_x2[1]),  11], [(hands_x1[10]-hands_x2[1]),  10], [(hands_x1[9]-hands_x2[1]),    9],
                    [(hands_x1[12]-hands_x2[2]),  12], [(hands_x1[11]-hands_x2[2]),  11], [(hands_x1[10]-hands_x2[2]),  10], [(hands_x1[9]-hands_x2[2]),    9],
                    [(hands_x1[12]-hands_x2[3]),  12], [(hands_x1[11]-hands_x2[3]),  11], [(hands_x1[10]-hands_x2[3]),  10], [(hands_x1[9]-hands_x2[3]),    9],
                    [(hands_x1[12]-hands_x2[4]),  12], [(hands_x1[11]-hands_x2[4]),  11], [(hands_x1[10]-hands_x2[4]),  10], [(hands_x1[9]-hands_x2[4]),    9],
                    [(hands_x1[12]-hands_x2[6]),  12], [(hands_x1[11]-hands_x2[5]),  11], [(hands_x1[10]-hands_x2[5]),  10], [(hands_x1[9]-hands_x2[5]),    9],
                    [(hands_x1[12]-hands_x2[6]),  12], [(hands_x1[11]-hands_x2[6]),  11], [(hands_x1[10]-hands_x2[6]),  10], [(hands_x1[9]-hands_x2[6]),    9],
                    [(hands_x1[12]-hands_x2[7]),  12], [(hands_x1[11]-hands_x2[7]),  11], [(hands_x1[10]-hands_x2[7]),  10], [(hands_x1[9]-hands_x2[7]),    9],
                    [(hands_x1[12]-hands_x2[8]),  12], [(hands_x1[11]-hands_x2[8]),  11], [(hands_x1[10]-hands_x2[8]),  10], [(hands_x1[9]-hands_x2[8]),    9],
                    [(hands_x1[12]-hands_x2[9]),  12], [(hands_x1[11]-hands_x2[9]),  11], [(hands_x1[10]-hands_x2[9]),  10], [(hands_x1[9]-hands_x2[9]),    9],
                    [(hands_x1[12]-hands_x2[10]), 12], [(hands_x1[11]-hands_x2[10]), 11], [(hands_x1[10]-hands_x2[10]), 10], [(hands_x1[9]-hands_x2[10]),   9],
                    [(hands_x1[12]-hands_x2[11]), 12], [(hands_x1[11]-hands_x2[11]), 11], [(hands_x1[10]-hands_x2[11]), 10], [(hands_x1[9]-hands_x2[11]),   9],
                    [(hands_x1[12]-hands_x2[12]), 12], [(hands_x1[11]-hands_x2[12]), 11], [(hands_x1[10]-hands_x2[12]), 10], [(hands_x1[9]-hands_x2[12]),   9],
                    [(hands_x1[12]-hands_x2[13]), 12], [(hands_x1[11]-hands_x2[13]), 11], [(hands_x1[10]-hands_x2[13]), 10], [(hands_x1[9]-hands_x2[13]),   9],
                    [(hands_x1[12]-hands_x2[14]), 12], [(hands_x1[11]-hands_x2[14]), 11], [(hands_x1[10]-hands_x2[14]), 10], [(hands_x1[9]-hands_x2[14]),   9],
                    [(hands_x1[12]-hands_x2[15]), 12], [(hands_x1[11]-hands_x2[15]), 11], [(hands_x1[10]-hands_x2[15]), 10], [(hands_x1[9]-hands_x2[15]),   9],
                    [(hands_x1[12]-hands_x2[16]), 12], [(hands_x1[11]-hands_x2[16]), 11], [(hands_x1[10]-hands_x2[16]), 10], [(hands_x1[9]-hands_x2[16]),   9],
                    [(hands_x1[12]-hands_x2[17]), 12], [(hands_x1[11]-hands_x2[17]), 11], [(hands_x1[10]-hands_x2[17]), 10], [(hands_x1[9]-hands_x2[17]),   9],
                    [(hands_x1[12]-hands_x2[18]), 12], [(hands_x1[11]-hands_x2[18]), 11], [(hands_x1[10]-hands_x2[18]), 10], [(hands_x1[9]-hands_x2[18]),   9],
                    [(hands_x1[12]-hands_x2[19]), 12], [(hands_x1[11]-hands_x2[19]), 11], [(hands_x1[10]-hands_x2[19]), 10], [(hands_x1[9]-hands_x2[19]),   9],
                    [(hands_x1[12]-hands_x2[20]), 12], [(hands_x1[11]-hands_x2[20]), 11], [(hands_x1[10]-hands_x2[20]), 10], [(hands_x1[9]-hands_x2[20]),   9],
                    #ring
                    [(hands_x1[16]-hands_x2[0]),  16], [(hands_x1[15]-hands_x2[0]),  15], [(hands_x1[14]-hands_x2[0]),  14], [(hands_x1[13]-hands_x2[0]),  13],
                    [(hands_x1[16]-hands_x2[1]),  16], [(hands_x1[15]-hands_x2[1]),  15], [(hands_x1[14]-hands_x2[1]),  14], [(hands_x1[13]-hands_x2[1]),  13],
                    [(hands_x1[16]-hands_x2[2]),  16], [(hands_x1[15]-hands_x2[2]),  15], [(hands_x1[14]-hands_x2[2]),  14], [(hands_x1[13]-hands_x2[2]),  13],
                    [(hands_x1[16]-hands_x2[3]),  16], [(hands_x1[15]-hands_x2[3]),  15], [(hands_x1[14]-hands_x2[3]),  14], [(hands_x1[13]-hands_x2[3]),  13],
                    [(hands_x1[16]-hands_x2[4]),  16], [(hands_x1[15]-hands_x2[4]),  15], [(hands_x1[14]-hands_x2[4]),  14], [(hands_x1[13]-hands_x2[4]),  13],
                    [(hands_x1[16]-hands_x2[6]),  16], [(hands_x1[15]-hands_x2[5]),  15], [(hands_x1[14]-hands_x2[5]),  14], [(hands_x1[13]-hands_x2[5]),  13],
                    [(hands_x1[16]-hands_x2[6]),  16], [(hands_x1[15]-hands_x2[6]),  15], [(hands_x1[14]-hands_x2[6]),  14], [(hands_x1[13]-hands_x2[6]),  13],
                    [(hands_x1[16]-hands_x2[7]),  16], [(hands_x1[15]-hands_x2[7]),  15], [(hands_x1[14]-hands_x2[7]),  14], [(hands_x1[13]-hands_x2[7]),  13],
                    [(hands_x1[16]-hands_x2[8]),  16], [(hands_x1[15]-hands_x2[8]),  15], [(hands_x1[14]-hands_x2[8]),  14], [(hands_x1[13]-hands_x2[8]),  13],
                    [(hands_x1[16]-hands_x2[9]),  16], [(hands_x1[15]-hands_x2[9]),  15], [(hands_x1[14]-hands_x2[9]),  14], [(hands_x1[13]-hands_x2[9]),  13],
                    [(hands_x1[16]-hands_x2[10]), 16], [(hands_x1[15]-hands_x2[10]), 15], [(hands_x1[14]-hands_x2[10]), 14], [(hands_x1[13]-hands_x2[10]), 13],
                    [(hands_x1[16]-hands_x2[11]), 16], [(hands_x1[15]-hands_x2[11]), 15], [(hands_x1[14]-hands_x2[11]), 14], [(hands_x1[13]-hands_x2[11]), 13],
                    [(hands_x1[16]-hands_x2[12]), 16], [(hands_x1[15]-hands_x2[12]), 15], [(hands_x1[14]-hands_x2[12]), 14], [(hands_x1[13]-hands_x2[12]), 13],
                    [(hands_x1[16]-hands_x2[13]), 16], [(hands_x1[15]-hands_x2[13]), 15], [(hands_x1[14]-hands_x2[13]), 14], [(hands_x1[13]-hands_x2[13]), 13],
                    [(hands_x1[16]-hands_x2[14]), 16], [(hands_x1[15]-hands_x2[14]), 15], [(hands_x1[14]-hands_x2[14]), 14], [(hands_x1[13]-hands_x2[14]), 13],
                    [(hands_x1[16]-hands_x2[15]), 16], [(hands_x1[15]-hands_x2[15]), 15], [(hands_x1[14]-hands_x2[15]), 14], [(hands_x1[13]-hands_x2[15]), 13],
                    [(hands_x1[16]-hands_x2[16]), 16], [(hands_x1[15]-hands_x2[16]), 15], [(hands_x1[14]-hands_x2[16]), 14], [(hands_x1[13]-hands_x2[16]), 13],
                    [(hands_x1[16]-hands_x2[17]), 16], [(hands_x1[15]-hands_x2[17]), 15], [(hands_x1[14]-hands_x2[17]), 14], [(hands_x1[13]-hands_x2[17]), 13],
                    [(hands_x1[16]-hands_x2[18]), 16], [(hands_x1[15]-hands_x2[18]), 15], [(hands_x1[14]-hands_x2[18]), 14], [(hands_x1[13]-hands_x2[18]), 13],
                    [(hands_x1[16]-hands_x2[19]), 16], [(hands_x1[15]-hands_x2[19]), 15], [(hands_x1[14]-hands_x2[19]), 14], [(hands_x1[13]-hands_x2[19]), 13],
                    [(hands_x1[16]-hands_x2[20]), 16], [(hands_x1[15]-hands_x2[20]), 15], [(hands_x1[14]-hands_x2[20]), 14], [(hands_x1[13]-hands_x2[20]), 13],
                    #pinky
                    [(hands_x1[20]-hands_x2[0]),  20], [(hands_x1[19]-hands_x2[0]),  19], [(hands_x1[18]-hands_x2[0]),  18], [(hands_x1[17]-hands_x2[0]),  17],
                    [(hands_x1[20]-hands_x2[1]),  20], [(hands_x1[19]-hands_x2[1]),  19], [(hands_x1[18]-hands_x2[1]),  18], [(hands_x1[17]-hands_x2[1]),  17],
                    [(hands_x1[20]-hands_x2[2]),  20], [(hands_x1[19]-hands_x2[2]),  19], [(hands_x1[18]-hands_x2[2]),  18], [(hands_x1[17]-hands_x2[2]),  17],
                    [(hands_x1[20]-hands_x2[3]),  20], [(hands_x1[19]-hands_x2[3]),  19], [(hands_x1[18]-hands_x2[3]),  18], [(hands_x1[17]-hands_x2[3]),  17],
                    [(hands_x1[20]-hands_x2[4]),  20], [(hands_x1[19]-hands_x2[4]),  19], [(hands_x1[18]-hands_x2[4]),  18], [(hands_x1[17]-hands_x2[4]),  17],
                    [(hands_x1[20]-hands_x2[6]),  20], [(hands_x1[19]-hands_x2[5]),  19], [(hands_x1[18]-hands_x2[5]),  18], [(hands_x1[17]-hands_x2[5]),  17],
                    [(hands_x1[20]-hands_x2[6]),  20], [(hands_x1[19]-hands_x2[6]),  19], [(hands_x1[18]-hands_x2[6]),  18], [(hands_x1[17]-hands_x2[6]),  17],
                    [(hands_x1[20]-hands_x2[7]),  20], [(hands_x1[19]-hands_x2[7]),  19], [(hands_x1[18]-hands_x2[7]),  18], [(hands_x1[17]-hands_x2[7]),  17],
                    [(hands_x1[20]-hands_x2[8]),  20], [(hands_x1[19]-hands_x2[8]),  19], [(hands_x1[18]-hands_x2[8]),  18], [(hands_x1[17]-hands_x2[8]),  17],
                    [(hands_x1[20]-hands_x2[9]),  20], [(hands_x1[19]-hands_x2[9]),  19], [(hands_x1[18]-hands_x2[9]),  18], [(hands_x1[17]-hands_x2[9]),  17],
                    [(hands_x1[20]-hands_x2[10]), 20], [(hands_x1[19]-hands_x2[10]), 19], [(hands_x1[18]-hands_x2[10]), 18], [(hands_x1[17]-hands_x2[10]), 17],
                    [(hands_x1[20]-hands_x2[11]), 20], [(hands_x1[19]-hands_x2[11]), 19], [(hands_x1[18]-hands_x2[11]), 18], [(hands_x1[17]-hands_x2[11]), 17],
                    [(hands_x1[20]-hands_x2[12]), 20], [(hands_x1[19]-hands_x2[12]), 19], [(hands_x1[18]-hands_x2[12]), 18], [(hands_x1[17]-hands_x2[12]), 17],
                    [(hands_x1[20]-hands_x2[13]), 20], [(hands_x1[19]-hands_x2[13]), 19], [(hands_x1[18]-hands_x2[13]), 18], [(hands_x1[17]-hands_x2[13]), 17],
                    [(hands_x1[20]-hands_x2[14]), 20], [(hands_x1[19]-hands_x2[14]), 19], [(hands_x1[18]-hands_x2[14]), 18], [(hands_x1[17]-hands_x2[14]), 17],
                    [(hands_x1[20]-hands_x2[15]), 20], [(hands_x1[19]-hands_x2[15]), 19], [(hands_x1[18]-hands_x2[15]), 18], [(hands_x1[17]-hands_x2[15]), 17],
                    [(hands_x1[20]-hands_x2[16]), 20], [(hands_x1[19]-hands_x2[16]), 19], [(hands_x1[18]-hands_x2[16]), 18], [(hands_x1[17]-hands_x2[16]), 17],
                    [(hands_x1[20]-hands_x2[17]), 20], [(hands_x1[19]-hands_x2[17]), 19], [(hands_x1[18]-hands_x2[17]), 18], [(hands_x1[17]-hands_x2[17]), 17],
                    [(hands_x1[20]-hands_x2[18]), 20], [(hands_x1[19]-hands_x2[18]), 19], [(hands_x1[18]-hands_x2[18]), 18], [(hands_x1[17]-hands_x2[18]), 17],
                    [(hands_x1[20]-hands_x2[19]), 20], [(hands_x1[19]-hands_x2[19]), 19], [(hands_x1[18]-hands_x2[19]), 18], [(hands_x1[17]-hands_x2[19]), 17],
                    [(hands_x1[20]-hands_x2[20]), 20], [(hands_x1[19]-hands_x2[20]), 19], [(hands_x1[18]-hands_x2[20]), 18], [(hands_x1[17]-hands_x2[20]), 17],
                    #wirst
                    [(hands_x1[0]-hands_x2[0]),    0],
                    [(hands_x1[0]-hands_x2[1]),    0],
                    [(hands_x1[0]-hands_x2[2]),    0],
                    [(hands_x1[0]-hands_x2[3]),    0],
                    [(hands_x1[0]-hands_x2[4]),    0],
                    [(hands_x1[0]-hands_x2[6]),    0],
                    [(hands_x1[0]-hands_x2[6]),    0],
                    [(hands_x1[0]-hands_x2[7]),    0],
                    [(hands_x1[0]-hands_x2[8]),    0],
                    [(hands_x1[0]-hands_x2[9]),    0],
                    [(hands_x1[0]-hands_x2[10]),   0],
                    [(hands_x1[0]-hands_x2[11]),   0],
                    [(hands_x1[0]-hands_x2[12]),   0],
                    [(hands_x1[0]-hands_x2[13]),   0],
                    [(hands_x1[0]-hands_x2[14]),   0],
                    [(hands_x1[0]-hands_x2[15]),   0],
                    [(hands_x1[0]-hands_x2[16]),   0],
                    [(hands_x1[0]-hands_x2[17]),   0],
                    [(hands_x1[0]-hands_x2[18]),   0],
                    [(hands_x1[0]-hands_x2[19]),   0],
                    [(hands_x1[0]-hands_x2[20]),   0]
                ]

                points_hand_relation_diffY = [
                    #thumb
                    [(hands_y1[4]-hands_y2[0]),    4], [(hands_y1[3]-hands_y2[0]),    3], [(hands_y1[2]-hands_y2[0]),    2], [(hands_y1[1]-hands_y2[0]),    1],
                    [(hands_y1[4]-hands_y2[1]),    4], [(hands_y1[3]-hands_y2[1]),    3], [(hands_y1[2]-hands_y2[1]),    2], [(hands_y1[1]-hands_y2[1]),    1],
                    [(hands_y1[4]-hands_y2[2]),    4], [(hands_y1[3]-hands_y2[2]),    3], [(hands_y1[2]-hands_y2[2]),    2], [(hands_y1[1]-hands_y2[2]),    1],
                    [(hands_y1[4]-hands_y2[3]),    4], [(hands_y1[3]-hands_y2[3]),    3], [(hands_y1[2]-hands_y2[3]),    2], [(hands_y1[1]-hands_y2[3]),    1],
                    [(hands_y1[4]-hands_y2[4]),    4], [(hands_y1[3]-hands_y2[4]),    3], [(hands_y1[2]-hands_y2[4]),    2], [(hands_y1[1]-hands_y2[4]),    1],
                    [(hands_y1[4]-hands_y2[6]),    4], [(hands_y1[3]-hands_y2[5]),    3], [(hands_y1[2]-hands_y2[5]),    2], [(hands_y1[1]-hands_y2[5]),    1],
                    [(hands_y1[4]-hands_y2[6]),    4], [(hands_y1[3]-hands_y2[6]),    3], [(hands_y1[2]-hands_y2[6]),    2], [(hands_y1[1]-hands_y2[6]),    1],
                    [(hands_y1[4]-hands_y2[7]),    4], [(hands_y1[3]-hands_y2[7]),    3], [(hands_y1[2]-hands_y2[7]),    2], [(hands_y1[1]-hands_y2[7]),    1],
                    [(hands_y1[4]-hands_y2[8]),    4], [(hands_y1[3]-hands_y2[8]),    3], [(hands_y1[2]-hands_y2[8]),    2], [(hands_y1[1]-hands_y2[8]),    1],
                    [(hands_y1[4]-hands_y2[9]),    4], [(hands_y1[3]-hands_y2[9]),    3], [(hands_y1[2]-hands_y2[9]),    2], [(hands_y1[1]-hands_y2[9]),    1],
                    [(hands_y1[4]-hands_y2[10]),   4], [(hands_y1[3]-hands_y2[10]),   3], [(hands_y1[2]-hands_y2[10]),   2], [(hands_y1[1]-hands_y2[10]),   1],
                    [(hands_y1[4]-hands_y2[11]),   4], [(hands_y1[3]-hands_y2[11]),   3], [(hands_y1[2]-hands_y2[11]),   2], [(hands_y1[1]-hands_y2[11]),   1],
                    [(hands_y1[4]-hands_y2[12]),   4], [(hands_y1[3]-hands_y2[12]),   3], [(hands_y1[2]-hands_y2[12]),   2], [(hands_y1[1]-hands_y2[12]),   1],
                    [(hands_y1[4]-hands_y2[13]),   4], [(hands_y1[3]-hands_y2[13]),   3], [(hands_y1[2]-hands_y2[13]),   2], [(hands_y1[1]-hands_y2[13]),   1],
                    [(hands_y1[4]-hands_y2[14]),   4], [(hands_y1[3]-hands_y2[14]),   3], [(hands_y1[2]-hands_y2[14]),   2], [(hands_y1[1]-hands_y2[14]),   1],
                    [(hands_y1[4]-hands_y2[15]),   4], [(hands_y1[3]-hands_y2[15]),   3], [(hands_y1[2]-hands_y2[15]),   2], [(hands_y1[1]-hands_y2[15]),   1],
                    [(hands_y1[4]-hands_y2[16]),   4], [(hands_y1[3]-hands_y2[16]),   3], [(hands_y1[2]-hands_y2[16]),   2], [(hands_y1[1]-hands_y2[16]),   1],
                    [(hands_y1[4]-hands_y2[17]),   4], [(hands_y1[3]-hands_y2[17]),   3], [(hands_y1[2]-hands_y2[17]),   2], [(hands_y1[1]-hands_y2[17]),   1],
                    [(hands_y1[4]-hands_y2[18]),   4], [(hands_y1[3]-hands_y2[18]),   3], [(hands_y1[2]-hands_y2[18]),   2], [(hands_y1[1]-hands_y2[18]),   1],
                    [(hands_y1[4]-hands_y2[19]),   4], [(hands_y1[3]-hands_y2[19]),   3], [(hands_y1[2]-hands_y2[19]),   2], [(hands_y1[1]-hands_y2[19]),   1],
                    [(hands_y1[4]-hands_y2[20]),   4], [(hands_y1[3]-hands_y2[20]),   3], [(hands_y1[2]-hands_y2[20]),   2], [(hands_y1[1]-hands_y2[20]),   1],
                    #index
                    [(hands_y1[8]-hands_y2[0]),    8], [(hands_y1[7]-hands_y2[0]),    7], [(hands_y1[6]-hands_y2[0]),    6], [(hands_y1[5]-hands_y2[0]),    5],
                    [(hands_y1[8]-hands_y2[1]),    8], [(hands_y1[7]-hands_y2[1]),    7], [(hands_y1[6]-hands_y2[1]),    6], [(hands_y1[5]-hands_y2[1]),    5],
                    [(hands_y1[8]-hands_y2[2]),    8], [(hands_y1[7]-hands_y2[2]),    7], [(hands_y1[6]-hands_y2[2]),    6], [(hands_y1[5]-hands_y2[2]),    5],
                    [(hands_y1[8]-hands_y2[3]),    8], [(hands_y1[7]-hands_y2[3]),    7], [(hands_y1[6]-hands_y2[3]),    6], [(hands_y1[5]-hands_y2[3]),    5],
                    [(hands_y1[8]-hands_y2[4]),    8], [(hands_y1[7]-hands_y2[4]),    7], [(hands_y1[6]-hands_y2[4]),    6], [(hands_y1[5]-hands_y2[4]),    5],
                    [(hands_y1[8]-hands_y2[6]),    8], [(hands_y1[7]-hands_y2[5]),    7], [(hands_y1[6]-hands_y2[5]),    6], [(hands_y1[5]-hands_y2[5]),    5],
                    [(hands_y1[8]-hands_y2[6]),    8], [(hands_y1[7]-hands_y2[6]),    7], [(hands_y1[6]-hands_y2[6]),    6], [(hands_y1[5]-hands_y2[6]),    5],
                    [(hands_y1[8]-hands_y2[7]),    8], [(hands_y1[7]-hands_y2[7]),    7], [(hands_y1[6]-hands_y2[7]),    6], [(hands_y1[5]-hands_y2[7]),    5],
                    [(hands_y1[8]-hands_y2[8]),    8], [(hands_y1[7]-hands_y2[8]),    7], [(hands_y1[6]-hands_y2[8]),    6], [(hands_y1[5]-hands_y2[8]),    5],
                    [(hands_y1[8]-hands_y2[9]),    8], [(hands_y1[7]-hands_y2[9]),    7], [(hands_y1[6]-hands_y2[9]),    6], [(hands_y1[5]-hands_y2[9]),    5],
                    [(hands_y1[8]-hands_y2[10]),   8], [(hands_y1[7]-hands_y2[10]),   7], [(hands_y1[6]-hands_y2[10]),   6], [(hands_y1[5]-hands_y2[10]),   5],
                    [(hands_y1[8]-hands_y2[11]),   8], [(hands_y1[7]-hands_y2[11]),   7], [(hands_y1[6]-hands_y2[11]),   6], [(hands_y1[5]-hands_y2[11]),   5],
                    [(hands_y1[8]-hands_y2[12]),   8], [(hands_y1[7]-hands_y2[12]),   7], [(hands_y1[6]-hands_y2[12]),   6], [(hands_y1[5]-hands_y2[12]),   5],
                    [(hands_y1[8]-hands_y2[13]),   8], [(hands_y1[7]-hands_y2[13]),   7], [(hands_y1[6]-hands_y2[13]),   6], [(hands_y1[5]-hands_y2[13]),   5],
                    [(hands_y1[8]-hands_y2[14]),   8], [(hands_y1[7]-hands_y2[14]),   7], [(hands_y1[6]-hands_y2[14]),   6], [(hands_y1[5]-hands_y2[14]),   5],
                    [(hands_y1[8]-hands_y2[15]),   8], [(hands_y1[7]-hands_y2[15]),   7], [(hands_y1[6]-hands_y2[15]),   6], [(hands_y1[5]-hands_y2[15]),   5],
                    [(hands_y1[8]-hands_y2[16]),   8], [(hands_y1[7]-hands_y2[16]),   7], [(hands_y1[6]-hands_y2[16]),   6], [(hands_y1[5]-hands_y2[16]),   5],
                    [(hands_y1[8]-hands_y2[17]),   8], [(hands_y1[7]-hands_y2[17]),   7], [(hands_y1[6]-hands_y2[17]),   6], [(hands_y1[5]-hands_y2[17]),   5],
                    [(hands_y1[8]-hands_y2[18]),   8], [(hands_y1[7]-hands_y2[18]),   7], [(hands_y1[6]-hands_y2[18]),   6], [(hands_y1[5]-hands_y2[18]),   5],
                    [(hands_y1[8]-hands_y2[19]),   8], [(hands_y1[7]-hands_y2[19]),   7], [(hands_y1[6]-hands_y2[19]),   6], [(hands_y1[5]-hands_y2[19]),   5],
                    [(hands_y1[8]-hands_y2[20]),   8], [(hands_y1[7]-hands_y2[20]),   7], [(hands_y1[6]-hands_y2[20]),   6], [(hands_y1[5]-hands_y2[20]),   5],
                    #middle
                    [(hands_y1[12]-hands_y2[0]),  12], [(hands_y1[11]-hands_y2[0]),  11], [(hands_y1[10]-hands_y2[0]),  10], [(hands_y1[9]-hands_y2[0]),    9],
                    [(hands_y1[12]-hands_y2[1]),  12], [(hands_y1[11]-hands_y2[1]),  11], [(hands_y1[10]-hands_y2[1]),  10], [(hands_y1[9]-hands_y2[1]),    9],
                    [(hands_y1[12]-hands_y2[2]),  12], [(hands_y1[11]-hands_y2[2]),  11], [(hands_y1[10]-hands_y2[2]),  10], [(hands_y1[9]-hands_y2[2]),    9],
                    [(hands_y1[12]-hands_y2[3]),  12], [(hands_y1[11]-hands_y2[3]),  11], [(hands_y1[10]-hands_y2[3]),  10], [(hands_y1[9]-hands_y2[3]),    9],
                    [(hands_y1[12]-hands_y2[4]),  12], [(hands_y1[11]-hands_y2[4]),  11], [(hands_y1[10]-hands_y2[4]),  10], [(hands_y1[9]-hands_y2[4]),    9],
                    [(hands_y1[12]-hands_y2[6]),  12], [(hands_y1[11]-hands_y2[5]),  11], [(hands_y1[10]-hands_y2[5]),  10], [(hands_y1[9]-hands_y2[5]),    9],
                    [(hands_y1[12]-hands_y2[6]),  12], [(hands_y1[11]-hands_y2[6]),  11], [(hands_y1[10]-hands_y2[6]),  10], [(hands_y1[9]-hands_y2[6]),    9],
                    [(hands_y1[12]-hands_y2[7]),  12], [(hands_y1[11]-hands_y2[7]),  11], [(hands_y1[10]-hands_y2[7]),  10], [(hands_y1[9]-hands_y2[7]),    9],
                    [(hands_y1[12]-hands_y2[8]),  12], [(hands_y1[11]-hands_y2[8]),  11], [(hands_y1[10]-hands_y2[8]),  10], [(hands_y1[9]-hands_y2[8]),    9],
                    [(hands_y1[12]-hands_y2[9]),  12], [(hands_y1[11]-hands_y2[9]),  11], [(hands_y1[10]-hands_y2[9]),  10], [(hands_y1[9]-hands_y2[9]),    9],
                    [(hands_y1[12]-hands_y2[10]), 12], [(hands_y1[11]-hands_y2[10]), 11], [(hands_y1[10]-hands_y2[10]), 10], [(hands_y1[9]-hands_y2[10]),   9],
                    [(hands_y1[12]-hands_y2[11]), 12], [(hands_y1[11]-hands_y2[11]), 11], [(hands_y1[10]-hands_y2[11]), 10], [(hands_y1[9]-hands_y2[11]),   9],
                    [(hands_y1[12]-hands_y2[12]), 12], [(hands_y1[11]-hands_y2[12]), 11], [(hands_y1[10]-hands_y2[12]), 10], [(hands_y1[9]-hands_y2[12]),   9],
                    [(hands_y1[12]-hands_y2[13]), 12], [(hands_y1[11]-hands_y2[13]), 11], [(hands_y1[10]-hands_y2[13]), 10], [(hands_y1[9]-hands_y2[13]),   9],
                    [(hands_y1[12]-hands_y2[14]), 12], [(hands_y1[11]-hands_y2[14]), 11], [(hands_y1[10]-hands_y2[14]), 10], [(hands_y1[9]-hands_y2[14]),   9],
                    [(hands_y1[12]-hands_y2[15]), 12], [(hands_y1[11]-hands_y2[15]), 11], [(hands_y1[10]-hands_y2[15]), 10], [(hands_y1[9]-hands_y2[15]),   9],
                    [(hands_y1[12]-hands_y2[16]), 12], [(hands_y1[11]-hands_y2[16]), 11], [(hands_y1[10]-hands_y2[16]), 10], [(hands_y1[9]-hands_y2[16]),   9],
                    [(hands_y1[12]-hands_y2[17]), 12], [(hands_y1[11]-hands_y2[17]), 11], [(hands_y1[10]-hands_y2[17]), 10], [(hands_y1[9]-hands_y2[17]),   9],
                    [(hands_y1[12]-hands_y2[18]), 12], [(hands_y1[11]-hands_y2[18]), 11], [(hands_y1[10]-hands_y2[18]), 10], [(hands_y1[9]-hands_y2[18]),   9],
                    [(hands_y1[12]-hands_y2[19]), 12], [(hands_y1[11]-hands_y2[19]), 11], [(hands_y1[10]-hands_y2[19]), 10], [(hands_y1[9]-hands_y2[19]),   9],
                    [(hands_y1[12]-hands_y2[20]), 12], [(hands_y1[11]-hands_y2[20]), 11], [(hands_y1[10]-hands_y2[20]), 10], [(hands_y1[9]-hands_y2[20]),   9],
                    #ring
                    [(hands_y1[16]-hands_y2[0]),  16], [(hands_y1[15]-hands_y2[0]),  15], [(hands_y1[14]-hands_y2[0]),  14], [(hands_y1[13]-hands_y2[0]),  13],
                    [(hands_y1[16]-hands_y2[1]),  16], [(hands_y1[15]-hands_y2[1]),  15], [(hands_y1[14]-hands_y2[1]),  14], [(hands_y1[13]-hands_y2[1]),  13],
                    [(hands_y1[16]-hands_y2[2]),  16], [(hands_y1[15]-hands_y2[2]),  15], [(hands_y1[14]-hands_y2[2]),  14], [(hands_y1[13]-hands_y2[2]),  13],
                    [(hands_y1[16]-hands_y2[3]),  16], [(hands_y1[15]-hands_y2[3]),  15], [(hands_y1[14]-hands_y2[3]),  14], [(hands_y1[13]-hands_y2[3]),  13],
                    [(hands_y1[16]-hands_y2[4]),  16], [(hands_y1[15]-hands_y2[4]),  15], [(hands_y1[14]-hands_y2[4]),  14], [(hands_y1[13]-hands_y2[4]),  13],
                    [(hands_y1[16]-hands_y2[6]),  16], [(hands_y1[15]-hands_y2[5]),  15], [(hands_y1[14]-hands_y2[5]),  14], [(hands_y1[13]-hands_y2[5]),  13],
                    [(hands_y1[16]-hands_y2[6]),  16], [(hands_y1[15]-hands_y2[6]),  15], [(hands_y1[14]-hands_y2[6]),  14], [(hands_y1[13]-hands_y2[6]),  13],
                    [(hands_y1[16]-hands_y2[7]),  16], [(hands_y1[15]-hands_y2[7]),  15], [(hands_y1[14]-hands_y2[7]),  14], [(hands_y1[13]-hands_y2[7]),  13],
                    [(hands_y1[16]-hands_y2[8]),  16], [(hands_y1[15]-hands_y2[8]),  15], [(hands_y1[14]-hands_y2[8]),  14], [(hands_y1[13]-hands_y2[8]),  13],
                    [(hands_y1[16]-hands_y2[9]),  16], [(hands_y1[15]-hands_y2[9]),  15], [(hands_y1[14]-hands_y2[9]),  14], [(hands_y1[13]-hands_y2[9]),  13],
                    [(hands_y1[16]-hands_y2[10]), 16], [(hands_y1[15]-hands_y2[10]), 15], [(hands_y1[14]-hands_y2[10]), 14], [(hands_y1[13]-hands_y2[10]), 13],
                    [(hands_y1[16]-hands_y2[11]), 16], [(hands_y1[15]-hands_y2[11]), 15], [(hands_y1[14]-hands_y2[11]), 14], [(hands_y1[13]-hands_y2[11]), 13],
                    [(hands_y1[16]-hands_y2[12]), 16], [(hands_y1[15]-hands_y2[12]), 15], [(hands_y1[14]-hands_y2[12]), 14], [(hands_y1[13]-hands_y2[12]), 13],
                    [(hands_y1[16]-hands_y2[13]), 16], [(hands_y1[15]-hands_y2[13]), 15], [(hands_y1[14]-hands_y2[13]), 14], [(hands_y1[13]-hands_y2[13]), 13],
                    [(hands_y1[16]-hands_y2[14]), 16], [(hands_y1[15]-hands_y2[14]), 15], [(hands_y1[14]-hands_y2[14]), 14], [(hands_y1[13]-hands_y2[14]), 13],
                    [(hands_y1[16]-hands_y2[15]), 16], [(hands_y1[15]-hands_y2[15]), 15], [(hands_y1[14]-hands_y2[15]), 14], [(hands_y1[13]-hands_y2[15]), 13],
                    [(hands_y1[16]-hands_y2[16]), 16], [(hands_y1[15]-hands_y2[16]), 15], [(hands_y1[14]-hands_y2[16]), 14], [(hands_y1[13]-hands_y2[16]), 13],
                    [(hands_y1[16]-hands_y2[17]), 16], [(hands_y1[15]-hands_y2[17]), 15], [(hands_y1[14]-hands_y2[17]), 14], [(hands_y1[13]-hands_y2[17]), 13],
                    [(hands_y1[16]-hands_y2[18]), 16], [(hands_y1[15]-hands_y2[18]), 15], [(hands_y1[14]-hands_y2[18]), 14], [(hands_y1[13]-hands_y2[18]), 13],
                    [(hands_y1[16]-hands_y2[19]), 16], [(hands_y1[15]-hands_y2[19]), 15], [(hands_y1[14]-hands_y2[19]), 14], [(hands_y1[13]-hands_y2[19]), 13],
                    [(hands_y1[16]-hands_y2[20]), 16], [(hands_y1[15]-hands_y2[20]), 15], [(hands_y1[14]-hands_y2[20]), 14], [(hands_y1[13]-hands_y2[20]), 13],
                    #pinky
                    [(hands_y1[20]-hands_y2[0]),  20], [(hands_y1[19]-hands_y2[0]),  19], [(hands_y1[18]-hands_y2[0]),  18], [(hands_y1[17]-hands_y2[0]),  17],
                    [(hands_y1[20]-hands_y2[1]),  20], [(hands_y1[19]-hands_y2[1]),  19], [(hands_y1[18]-hands_y2[1]),  18], [(hands_y1[17]-hands_y2[1]),  17],
                    [(hands_y1[20]-hands_y2[2]),  20], [(hands_y1[19]-hands_y2[2]),  19], [(hands_y1[18]-hands_y2[2]),  18], [(hands_y1[17]-hands_y2[2]),  17],
                    [(hands_y1[20]-hands_y2[3]),  20], [(hands_y1[19]-hands_y2[3]),  19], [(hands_y1[18]-hands_y2[3]),  18], [(hands_y1[17]-hands_y2[3]),  17],
                    [(hands_y1[20]-hands_y2[4]),  20], [(hands_y1[19]-hands_y2[4]),  19], [(hands_y1[18]-hands_y2[4]),  18], [(hands_y1[17]-hands_y2[4]),  17],
                    [(hands_y1[20]-hands_y2[6]),  20], [(hands_y1[19]-hands_y2[5]),  19], [(hands_y1[18]-hands_y2[5]),  18], [(hands_y1[17]-hands_y2[5]),  17],
                    [(hands_y1[20]-hands_y2[6]),  20], [(hands_y1[19]-hands_y2[6]),  19], [(hands_y1[18]-hands_y2[6]),  18], [(hands_y1[17]-hands_y2[6]),  17],
                    [(hands_y1[20]-hands_y2[7]),  20], [(hands_y1[19]-hands_y2[7]),  19], [(hands_y1[18]-hands_y2[7]),  18], [(hands_y1[17]-hands_y2[7]),  17],
                    [(hands_y1[20]-hands_y2[8]),  20], [(hands_y1[19]-hands_y2[8]),  19], [(hands_y1[18]-hands_y2[8]),  18], [(hands_y1[17]-hands_y2[8]),  17],
                    [(hands_y1[20]-hands_y2[9]),  20], [(hands_y1[19]-hands_y2[9]),  19], [(hands_y1[18]-hands_y2[9]),  18], [(hands_y1[17]-hands_y2[9]),  17],
                    [(hands_y1[20]-hands_y2[10]), 20], [(hands_y1[19]-hands_y2[10]), 19], [(hands_y1[18]-hands_y2[10]), 18], [(hands_y1[17]-hands_y2[10]), 17],
                    [(hands_y1[20]-hands_y2[11]), 20], [(hands_y1[19]-hands_y2[11]), 19], [(hands_y1[18]-hands_y2[11]), 18], [(hands_y1[17]-hands_y2[11]), 17],
                    [(hands_y1[20]-hands_y2[12]), 20], [(hands_y1[19]-hands_y2[12]), 19], [(hands_y1[18]-hands_y2[12]), 18], [(hands_y1[17]-hands_y2[12]), 17],
                    [(hands_y1[20]-hands_y2[13]), 20], [(hands_y1[19]-hands_y2[13]), 19], [(hands_y1[18]-hands_y2[13]), 18], [(hands_y1[17]-hands_y2[13]), 17],
                    [(hands_y1[20]-hands_y2[14]), 20], [(hands_y1[19]-hands_y2[14]), 19], [(hands_y1[18]-hands_y2[14]), 18], [(hands_y1[17]-hands_y2[14]), 17],
                    [(hands_y1[20]-hands_y2[15]), 20], [(hands_y1[19]-hands_y2[15]), 19], [(hands_y1[18]-hands_y2[15]), 18], [(hands_y1[17]-hands_y2[15]), 17],
                    [(hands_y1[20]-hands_y2[16]), 20], [(hands_y1[19]-hands_y2[16]), 19], [(hands_y1[18]-hands_y2[16]), 18], [(hands_y1[17]-hands_y2[16]), 17],
                    [(hands_y1[20]-hands_y2[17]), 20], [(hands_y1[19]-hands_y2[17]), 19], [(hands_y1[18]-hands_y2[17]), 18], [(hands_y1[17]-hands_y2[17]), 17],
                    [(hands_y1[20]-hands_y2[18]), 20], [(hands_y1[19]-hands_y2[18]), 19], [(hands_y1[18]-hands_y2[18]), 18], [(hands_y1[17]-hands_y2[18]), 17],
                    [(hands_y1[20]-hands_y2[19]), 20], [(hands_y1[19]-hands_y2[19]), 19], [(hands_y1[18]-hands_y2[19]), 18], [(hands_y1[17]-hands_y2[19]), 17],
                    [(hands_y1[20]-hands_y2[20]), 20], [(hands_y1[19]-hands_y2[20]), 19], [(hands_y1[18]-hands_y2[20]), 18], [(hands_y1[17]-hands_y2[20]), 17],
                    #wirst
                    [(hands_y1[0]-hands_y2[0]),    0],
                    [(hands_y1[0]-hands_y2[1]),    0],
                    [(hands_y1[0]-hands_y2[2]),    0],
                    [(hands_y1[0]-hands_y2[3]),    0],
                    [(hands_y1[0]-hands_y2[4]),    0],
                    [(hands_y1[0]-hands_y2[6]),    0],
                    [(hands_y1[0]-hands_y2[6]),    0],
                    [(hands_y1[0]-hands_y2[7]),    0],
                    [(hands_y1[0]-hands_y2[8]),    0],
                    [(hands_y1[0]-hands_y2[9]),    0],
                    [(hands_y1[0]-hands_y2[10]),   0],
                    [(hands_y1[0]-hands_y2[11]),   0],
                    [(hands_y1[0]-hands_y2[12]),   0],
                    [(hands_y1[0]-hands_y2[13]),   0],
                    [(hands_y1[0]-hands_y2[14]),   0],
                    [(hands_y1[0]-hands_y2[15]),   0],
                    [(hands_y1[0]-hands_y2[16]),   0],
                    [(hands_y1[0]-hands_y2[17]),   0],
                    [(hands_y1[0]-hands_y2[18]),   0],
                    [(hands_y1[0]-hands_y2[19]),   0],
                    [(hands_y1[0]-hands_y2[20]),   0]
                ]
            
                points_hand_relation_diffZ = [
                    #thumb
                    [(hands_z1[4]-hands_z2[0]),    4], [(hands_z1[3]-hands_z2[0]),    3], [(hands_z1[2]-hands_z2[0]),    2], [(hands_z1[1]-hands_z2[0]),    1],
                    [(hands_z1[4]-hands_z2[1]),    4], [(hands_z1[3]-hands_z2[1]),    3], [(hands_z1[2]-hands_z2[1]),    2], [(hands_z1[1]-hands_z2[1]),    1],
                    [(hands_z1[4]-hands_z2[2]),    4], [(hands_z1[3]-hands_z2[2]),    3], [(hands_z1[2]-hands_z2[2]),    2], [(hands_z1[1]-hands_z2[2]),    1],
                    [(hands_z1[4]-hands_z2[3]),    4], [(hands_z1[3]-hands_z2[3]),    3], [(hands_z1[2]-hands_z2[3]),    2], [(hands_z1[1]-hands_z2[3]),    1],
                    [(hands_z1[4]-hands_z2[4]),    4], [(hands_z1[3]-hands_z2[4]),    3], [(hands_z1[2]-hands_z2[4]),    2], [(hands_z1[1]-hands_z2[4]),    1],
                    [(hands_z1[4]-hands_z2[6]),    4], [(hands_z1[3]-hands_z2[5]),    3], [(hands_z1[2]-hands_z2[5]),    2], [(hands_z1[1]-hands_z2[5]),    1],
                    [(hands_z1[4]-hands_z2[6]),    4], [(hands_z1[3]-hands_z2[6]),    3], [(hands_z1[2]-hands_z2[6]),    2], [(hands_z1[1]-hands_z2[6]),    1],
                    [(hands_z1[4]-hands_z2[7]),    4], [(hands_z1[3]-hands_z2[7]),    3], [(hands_z1[2]-hands_z2[7]),    2], [(hands_z1[1]-hands_z2[7]),    1],
                    [(hands_z1[4]-hands_z2[8]),    4], [(hands_z1[3]-hands_z2[8]),    3], [(hands_z1[2]-hands_z2[8]),    2], [(hands_z1[1]-hands_z2[8]),    1],
                    [(hands_z1[4]-hands_z2[9]),    4], [(hands_z1[3]-hands_z2[9]),    3], [(hands_z1[2]-hands_z2[9]),    2], [(hands_z1[1]-hands_z2[9]),    1],
                    [(hands_z1[4]-hands_z2[10]),   4], [(hands_z1[3]-hands_z2[10]),   3], [(hands_z1[2]-hands_z2[10]),   2], [(hands_z1[1]-hands_z2[10]),   1],
                    [(hands_z1[4]-hands_z2[11]),   4], [(hands_z1[3]-hands_z2[11]),   3], [(hands_z1[2]-hands_z2[11]),   2], [(hands_z1[1]-hands_z2[11]),   1],
                    [(hands_z1[4]-hands_z2[12]),   4], [(hands_z1[3]-hands_z2[12]),   3], [(hands_z1[2]-hands_z2[12]),   2], [(hands_z1[1]-hands_z2[12]),   1],
                    [(hands_z1[4]-hands_z2[13]),   4], [(hands_z1[3]-hands_z2[13]),   3], [(hands_z1[2]-hands_z2[13]),   2], [(hands_z1[1]-hands_z2[13]),   1],
                    [(hands_z1[4]-hands_z2[14]),   4], [(hands_z1[3]-hands_z2[14]),   3], [(hands_z1[2]-hands_z2[14]),   2], [(hands_z1[1]-hands_z2[14]),   1],
                    [(hands_z1[4]-hands_z2[15]),   4], [(hands_z1[3]-hands_z2[15]),   3], [(hands_z1[2]-hands_z2[15]),   2], [(hands_z1[1]-hands_z2[15]),   1],
                    [(hands_z1[4]-hands_z2[16]),   4], [(hands_z1[3]-hands_z2[16]),   3], [(hands_z1[2]-hands_z2[16]),   2], [(hands_z1[1]-hands_z2[16]),   1],
                    [(hands_z1[4]-hands_z2[17]),   4], [(hands_z1[3]-hands_z2[17]),   3], [(hands_z1[2]-hands_z2[17]),   2], [(hands_z1[1]-hands_z2[17]),   1],
                    [(hands_z1[4]-hands_z2[18]),   4], [(hands_z1[3]-hands_z2[18]),   3], [(hands_z1[2]-hands_z2[18]),   2], [(hands_z1[1]-hands_z2[18]),   1],
                    [(hands_z1[4]-hands_z2[19]),   4], [(hands_z1[3]-hands_z2[19]),   3], [(hands_z1[2]-hands_z2[19]),   2], [(hands_z1[1]-hands_z2[19]),   1],
                    [(hands_z1[4]-hands_z2[20]),   4], [(hands_z1[3]-hands_z2[20]),   3], [(hands_z1[2]-hands_z2[20]),   2], [(hands_z1[1]-hands_z2[20]),   1],
                    #index
                    [(hands_z1[8]-hands_z2[0]),    8], [(hands_z1[7]-hands_z2[0]),    7], [(hands_z1[6]-hands_z2[0]),    6], [(hands_z1[5]-hands_z2[0]),    5],
                    [(hands_z1[8]-hands_z2[1]),    8], [(hands_z1[7]-hands_z2[1]),    7], [(hands_z1[6]-hands_z2[1]),    6], [(hands_z1[5]-hands_z2[1]),    5],
                    [(hands_z1[8]-hands_z2[2]),    8], [(hands_z1[7]-hands_z2[2]),    7], [(hands_z1[6]-hands_z2[2]),    6], [(hands_z1[5]-hands_z2[2]),    5],
                    [(hands_z1[8]-hands_z2[3]),    8], [(hands_z1[7]-hands_z2[3]),    7], [(hands_z1[6]-hands_z2[3]),    6], [(hands_z1[5]-hands_z2[3]),    5],
                    [(hands_z1[8]-hands_z2[4]),    8], [(hands_z1[7]-hands_z2[4]),    7], [(hands_z1[6]-hands_z2[4]),    6], [(hands_z1[5]-hands_z2[4]),    5],
                    [(hands_z1[8]-hands_z2[6]),    8], [(hands_z1[7]-hands_z2[5]),    7], [(hands_z1[6]-hands_z2[5]),    6], [(hands_z1[5]-hands_z2[5]),    5],
                    [(hands_z1[8]-hands_z2[6]),    8], [(hands_z1[7]-hands_z2[6]),    7], [(hands_z1[6]-hands_z2[6]),    6], [(hands_z1[5]-hands_z2[6]),    5],
                    [(hands_z1[8]-hands_z2[7]),    8], [(hands_z1[7]-hands_z2[7]),    7], [(hands_z1[6]-hands_z2[7]),    6], [(hands_z1[5]-hands_z2[7]),    5],
                    [(hands_z1[8]-hands_z2[8]),    8], [(hands_z1[7]-hands_z2[8]),    7], [(hands_z1[6]-hands_z2[8]),    6], [(hands_z1[5]-hands_z2[8]),    5],
                    [(hands_z1[8]-hands_z2[9]),    8], [(hands_z1[7]-hands_z2[9]),    7], [(hands_z1[6]-hands_z2[9]),    6], [(hands_z1[5]-hands_z2[9]),    5],
                    [(hands_z1[8]-hands_z2[10]),   8], [(hands_z1[7]-hands_z2[10]),   7], [(hands_z1[6]-hands_z2[10]),   6], [(hands_z1[5]-hands_z2[10]),   5],
                    [(hands_z1[8]-hands_z2[11]),   8], [(hands_z1[7]-hands_z2[11]),   7], [(hands_z1[6]-hands_z2[11]),   6], [(hands_z1[5]-hands_z2[11]),   5],
                    [(hands_z1[8]-hands_z2[12]),   8], [(hands_z1[7]-hands_z2[12]),   7], [(hands_z1[6]-hands_z2[12]),   6], [(hands_z1[5]-hands_z2[12]),   5],
                    [(hands_z1[8]-hands_z2[13]),   8], [(hands_z1[7]-hands_z2[13]),   7], [(hands_z1[6]-hands_z2[13]),   6], [(hands_z1[5]-hands_z2[13]),   5],
                    [(hands_z1[8]-hands_z2[14]),   8], [(hands_z1[7]-hands_z2[14]),   7], [(hands_z1[6]-hands_z2[14]),   6], [(hands_z1[5]-hands_z2[14]),   5],
                    [(hands_z1[8]-hands_z2[15]),   8], [(hands_z1[7]-hands_z2[15]),   7], [(hands_z1[6]-hands_z2[15]),   6], [(hands_z1[5]-hands_z2[15]),   5],
                    [(hands_z1[8]-hands_z2[16]),   8], [(hands_z1[7]-hands_z2[16]),   7], [(hands_z1[6]-hands_z2[16]),   6], [(hands_z1[5]-hands_z2[16]),   5],
                    [(hands_z1[8]-hands_z2[17]),   8], [(hands_z1[7]-hands_z2[17]),   7], [(hands_z1[6]-hands_z2[17]),   6], [(hands_z1[5]-hands_z2[17]),   5],
                    [(hands_z1[8]-hands_z2[18]),   8], [(hands_z1[7]-hands_z2[18]),   7], [(hands_z1[6]-hands_z2[18]),   6], [(hands_z1[5]-hands_z2[18]),   5],
                    [(hands_z1[8]-hands_z2[19]),   8], [(hands_z1[7]-hands_z2[19]),   7], [(hands_z1[6]-hands_z2[19]),   6], [(hands_z1[5]-hands_z2[19]),   5],
                    [(hands_z1[8]-hands_z2[20]),   8], [(hands_z1[7]-hands_z2[20]),   7], [(hands_z1[6]-hands_z2[20]),   6], [(hands_z1[5]-hands_z2[20]),   5],
                    #middle
                    [(hands_z1[12]-hands_z2[0]),  12], [(hands_z1[11]-hands_z2[0]),  11], [(hands_z1[10]-hands_z2[0]),  10], [(hands_z1[9]-hands_z2[0]),    9],
                    [(hands_z1[12]-hands_z2[1]),  12], [(hands_z1[11]-hands_z2[1]),  11], [(hands_z1[10]-hands_z2[1]),  10], [(hands_z1[9]-hands_z2[1]),    9],
                    [(hands_z1[12]-hands_z2[2]),  12], [(hands_z1[11]-hands_z2[2]),  11], [(hands_z1[10]-hands_z2[2]),  10], [(hands_z1[9]-hands_z2[2]),    9],
                    [(hands_z1[12]-hands_z2[3]),  12], [(hands_z1[11]-hands_z2[3]),  11], [(hands_z1[10]-hands_z2[3]),  10], [(hands_z1[9]-hands_z2[3]),    9],
                    [(hands_z1[12]-hands_z2[4]),  12], [(hands_z1[11]-hands_z2[4]),  11], [(hands_z1[10]-hands_z2[4]),  10], [(hands_z1[9]-hands_z2[4]),    9],
                    [(hands_z1[12]-hands_z2[6]),  12], [(hands_z1[11]-hands_z2[5]),  11], [(hands_z1[10]-hands_z2[5]),  10], [(hands_z1[9]-hands_z2[5]),    9],
                    [(hands_z1[12]-hands_z2[6]),  12], [(hands_z1[11]-hands_z2[6]),  11], [(hands_z1[10]-hands_z2[6]),  10], [(hands_z1[9]-hands_z2[6]),    9],
                    [(hands_z1[12]-hands_z2[7]),  12], [(hands_z1[11]-hands_z2[7]),  11], [(hands_z1[10]-hands_z2[7]),  10], [(hands_z1[9]-hands_z2[7]),    9],
                    [(hands_z1[12]-hands_z2[8]),  12], [(hands_z1[11]-hands_z2[8]),  11], [(hands_z1[10]-hands_z2[8]),  10], [(hands_z1[9]-hands_z2[8]),    9],
                    [(hands_z1[12]-hands_z2[9]),  12], [(hands_z1[11]-hands_z2[9]),  11], [(hands_z1[10]-hands_z2[9]),  10], [(hands_z1[9]-hands_z2[9]),    9],
                    [(hands_z1[12]-hands_z2[10]), 12], [(hands_z1[11]-hands_z2[10]), 11], [(hands_z1[10]-hands_z2[10]), 10], [(hands_z1[9]-hands_z2[10]),   9],
                    [(hands_z1[12]-hands_z2[11]), 12], [(hands_z1[11]-hands_z2[11]), 11], [(hands_z1[10]-hands_z2[11]), 10], [(hands_z1[9]-hands_z2[11]),   9],
                    [(hands_z1[12]-hands_z2[12]), 12], [(hands_z1[11]-hands_z2[12]), 11], [(hands_z1[10]-hands_z2[12]), 10], [(hands_z1[9]-hands_z2[12]),   9],
                    [(hands_z1[12]-hands_z2[13]), 12], [(hands_z1[11]-hands_z2[13]), 11], [(hands_z1[10]-hands_z2[13]), 10], [(hands_z1[9]-hands_z2[13]),   9],
                    [(hands_z1[12]-hands_z2[14]), 12], [(hands_z1[11]-hands_z2[14]), 11], [(hands_z1[10]-hands_z2[14]), 10], [(hands_z1[9]-hands_z2[14]),   9],
                    [(hands_z1[12]-hands_z2[15]), 12], [(hands_z1[11]-hands_z2[15]), 11], [(hands_z1[10]-hands_z2[15]), 10], [(hands_z1[9]-hands_z2[15]),   9],
                    [(hands_z1[12]-hands_z2[16]), 12], [(hands_z1[11]-hands_z2[16]), 11], [(hands_z1[10]-hands_z2[16]), 10], [(hands_z1[9]-hands_z2[16]),   9],
                    [(hands_z1[12]-hands_z2[17]), 12], [(hands_z1[11]-hands_z2[17]), 11], [(hands_z1[10]-hands_z2[17]), 10], [(hands_z1[9]-hands_z2[17]),   9],
                    [(hands_z1[12]-hands_z2[18]), 12], [(hands_z1[11]-hands_z2[18]), 11], [(hands_z1[10]-hands_z2[18]), 10], [(hands_z1[9]-hands_z2[18]),   9],
                    [(hands_z1[12]-hands_z2[19]), 12], [(hands_z1[11]-hands_z2[19]), 11], [(hands_z1[10]-hands_z2[19]), 10], [(hands_z1[9]-hands_z2[19]),   9],
                    [(hands_z1[12]-hands_z2[20]), 12], [(hands_z1[11]-hands_z2[20]), 11], [(hands_z1[10]-hands_z2[20]), 10], [(hands_z1[9]-hands_z2[20]),   9],
                    #ring
                    [(hands_z1[16]-hands_z2[0]),  16], [(hands_z1[15]-hands_z2[0]),  15], [(hands_z1[14]-hands_z2[0]),  14], [(hands_z1[13]-hands_z2[0]),  13],
                    [(hands_z1[16]-hands_z2[1]),  16], [(hands_z1[15]-hands_z2[1]),  15], [(hands_z1[14]-hands_z2[1]),  14], [(hands_z1[13]-hands_z2[1]),  13],
                    [(hands_z1[16]-hands_z2[2]),  16], [(hands_z1[15]-hands_z2[2]),  15], [(hands_z1[14]-hands_z2[2]),  14], [(hands_z1[13]-hands_z2[2]),  13],
                    [(hands_z1[16]-hands_z2[3]),  16], [(hands_z1[15]-hands_z2[3]),  15], [(hands_z1[14]-hands_z2[3]),  14], [(hands_z1[13]-hands_z2[3]),  13],
                    [(hands_z1[16]-hands_z2[4]),  16], [(hands_z1[15]-hands_z2[4]),  15], [(hands_z1[14]-hands_z2[4]),  14], [(hands_z1[13]-hands_z2[4]),  13],
                    [(hands_z1[16]-hands_z2[6]),  16], [(hands_z1[15]-hands_z2[5]),  15], [(hands_z1[14]-hands_z2[5]),  14], [(hands_z1[13]-hands_z2[5]),  13],
                    [(hands_z1[16]-hands_z2[6]),  16], [(hands_z1[15]-hands_z2[6]),  15], [(hands_z1[14]-hands_z2[6]),  14], [(hands_z1[13]-hands_z2[6]),  13],
                    [(hands_z1[16]-hands_z2[7]),  16], [(hands_z1[15]-hands_z2[7]),  15], [(hands_z1[14]-hands_z2[7]),  14], [(hands_z1[13]-hands_z2[7]),  13],
                    [(hands_z1[16]-hands_z2[8]),  16], [(hands_z1[15]-hands_z2[8]),  15], [(hands_z1[14]-hands_z2[8]),  14], [(hands_z1[13]-hands_z2[8]),  13],
                    [(hands_z1[16]-hands_z2[9]),  16], [(hands_z1[15]-hands_z2[9]),  15], [(hands_z1[14]-hands_z2[9]),  14], [(hands_z1[13]-hands_z2[9]),  13],
                    [(hands_z1[16]-hands_z2[10]), 16], [(hands_z1[15]-hands_z2[10]), 15], [(hands_z1[14]-hands_z2[10]), 14], [(hands_z1[13]-hands_z2[10]), 13],
                    [(hands_z1[16]-hands_z2[11]), 16], [(hands_z1[15]-hands_z2[11]), 15], [(hands_z1[14]-hands_z2[11]), 14], [(hands_z1[13]-hands_z2[11]), 13],
                    [(hands_z1[16]-hands_z2[12]), 16], [(hands_z1[15]-hands_z2[12]), 15], [(hands_z1[14]-hands_z2[12]), 14], [(hands_z1[13]-hands_z2[12]), 13],
                    [(hands_z1[16]-hands_z2[13]), 16], [(hands_z1[15]-hands_z2[13]), 15], [(hands_z1[14]-hands_z2[13]), 14], [(hands_z1[13]-hands_z2[13]), 13],
                    [(hands_z1[16]-hands_z2[14]), 16], [(hands_z1[15]-hands_z2[14]), 15], [(hands_z1[14]-hands_z2[14]), 14], [(hands_z1[13]-hands_z2[14]), 13],
                    [(hands_z1[16]-hands_z2[15]), 16], [(hands_z1[15]-hands_z2[15]), 15], [(hands_z1[14]-hands_z2[15]), 14], [(hands_z1[13]-hands_z2[15]), 13],
                    [(hands_z1[16]-hands_z2[16]), 16], [(hands_z1[15]-hands_z2[16]), 15], [(hands_z1[14]-hands_z2[16]), 14], [(hands_z1[13]-hands_z2[16]), 13],
                    [(hands_z1[16]-hands_z2[17]), 16], [(hands_z1[15]-hands_z2[17]), 15], [(hands_z1[14]-hands_z2[17]), 14], [(hands_z1[13]-hands_z2[17]), 13],
                    [(hands_z1[16]-hands_z2[18]), 16], [(hands_z1[15]-hands_z2[18]), 15], [(hands_z1[14]-hands_z2[18]), 14], [(hands_z1[13]-hands_z2[18]), 13],
                    [(hands_z1[16]-hands_z2[19]), 16], [(hands_z1[15]-hands_z2[19]), 15], [(hands_z1[14]-hands_z2[19]), 14], [(hands_z1[13]-hands_z2[19]), 13],
                    [(hands_z1[16]-hands_z2[20]), 16], [(hands_z1[15]-hands_z2[20]), 15], [(hands_z1[14]-hands_z2[20]), 14], [(hands_z1[13]-hands_z2[20]), 13],
                    #pinky
                    [(hands_z1[20]-hands_z2[0]),  20], [(hands_z1[19]-hands_z2[0]),  19], [(hands_z1[18]-hands_z2[0]),  18], [(hands_z1[17]-hands_z2[0]),  17],
                    [(hands_z1[20]-hands_z2[1]),  20], [(hands_z1[19]-hands_z2[1]),  19], [(hands_z1[18]-hands_z2[1]),  18], [(hands_z1[17]-hands_z2[1]),  17],
                    [(hands_z1[20]-hands_z2[2]),  20], [(hands_z1[19]-hands_z2[2]),  19], [(hands_z1[18]-hands_z2[2]),  18], [(hands_z1[17]-hands_z2[2]),  17],
                    [(hands_z1[20]-hands_z2[3]),  20], [(hands_z1[19]-hands_z2[3]),  19], [(hands_z1[18]-hands_z2[3]),  18], [(hands_z1[17]-hands_z2[3]),  17],
                    [(hands_z1[20]-hands_z2[4]),  20], [(hands_z1[19]-hands_z2[4]),  19], [(hands_z1[18]-hands_z2[4]),  18], [(hands_z1[17]-hands_z2[4]),  17],
                    [(hands_z1[20]-hands_z2[6]),  20], [(hands_z1[19]-hands_z2[5]),  19], [(hands_z1[18]-hands_z2[5]),  18], [(hands_z1[17]-hands_z2[5]),  17],
                    [(hands_z1[20]-hands_z2[6]),  20], [(hands_z1[19]-hands_z2[6]),  19], [(hands_z1[18]-hands_z2[6]),  18], [(hands_z1[17]-hands_z2[6]),  17],
                    [(hands_z1[20]-hands_z2[7]),  20], [(hands_z1[19]-hands_z2[7]),  19], [(hands_z1[18]-hands_z2[7]),  18], [(hands_z1[17]-hands_z2[7]),  17],
                    [(hands_z1[20]-hands_z2[8]),  20], [(hands_z1[19]-hands_z2[8]),  19], [(hands_z1[18]-hands_z2[8]),  18], [(hands_z1[17]-hands_z2[8]),  17],
                    [(hands_z1[20]-hands_z2[9]),  20], [(hands_z1[19]-hands_z2[9]),  19], [(hands_z1[18]-hands_z2[9]),  18], [(hands_z1[17]-hands_z2[9]),  17],
                    [(hands_z1[20]-hands_z2[10]), 20], [(hands_z1[19]-hands_z2[10]), 19], [(hands_z1[18]-hands_z2[10]), 18], [(hands_z1[17]-hands_z2[10]), 17],
                    [(hands_z1[20]-hands_z2[11]), 20], [(hands_z1[19]-hands_z2[11]), 19], [(hands_z1[18]-hands_z2[11]), 18], [(hands_z1[17]-hands_z2[11]), 17],
                    [(hands_z1[20]-hands_z2[12]), 20], [(hands_z1[19]-hands_z2[12]), 19], [(hands_z1[18]-hands_z2[12]), 18], [(hands_z1[17]-hands_z2[12]), 17],
                    [(hands_z1[20]-hands_z2[13]), 20], [(hands_z1[19]-hands_z2[13]), 19], [(hands_z1[18]-hands_z2[13]), 18], [(hands_z1[17]-hands_z2[13]), 17],
                    [(hands_z1[20]-hands_z2[14]), 20], [(hands_z1[19]-hands_z2[14]), 19], [(hands_z1[18]-hands_z2[14]), 18], [(hands_z1[17]-hands_z2[14]), 17],
                    [(hands_z1[20]-hands_z2[15]), 20], [(hands_z1[19]-hands_z2[15]), 19], [(hands_z1[18]-hands_z2[15]), 18], [(hands_z1[17]-hands_z2[15]), 17],
                    [(hands_z1[20]-hands_z2[16]), 20], [(hands_z1[19]-hands_z2[16]), 19], [(hands_z1[18]-hands_z2[16]), 18], [(hands_z1[17]-hands_z2[16]), 17],
                    [(hands_z1[20]-hands_z2[17]), 20], [(hands_z1[19]-hands_z2[17]), 19], [(hands_z1[18]-hands_z2[17]), 18], [(hands_z1[17]-hands_z2[17]), 17],
                    [(hands_z1[20]-hands_z2[18]), 20], [(hands_z1[19]-hands_z2[18]), 19], [(hands_z1[18]-hands_z2[18]), 18], [(hands_z1[17]-hands_z2[18]), 17],
                    [(hands_z1[20]-hands_z2[19]), 20], [(hands_z1[19]-hands_z2[19]), 19], [(hands_z1[18]-hands_z2[19]), 18], [(hands_z1[17]-hands_z2[19]), 17],
                    [(hands_z1[20]-hands_z2[20]), 20], [(hands_z1[19]-hands_z2[20]), 19], [(hands_z1[18]-hands_z2[20]), 18], [(hands_z1[17]-hands_z2[20]), 17],
                    #wirst
                    [(hands_z1[0]-hands_z2[0]),    0],
                    [(hands_z1[0]-hands_z2[1]),    0],
                    [(hands_z1[0]-hands_z2[2]),    0],
                    [(hands_z1[0]-hands_z2[3]),    0],
                    [(hands_z1[0]-hands_z2[4]),    0],
                    [(hands_z1[0]-hands_z2[6]),    0],
                    [(hands_z1[0]-hands_z2[6]),    0],
                    [(hands_z1[0]-hands_z2[7]),    0],
                    [(hands_z1[0]-hands_z2[8]),    0],
                    [(hands_z1[0]-hands_z2[9]),    0],
                    [(hands_z1[0]-hands_z2[10]),   0],
                    [(hands_z1[0]-hands_z2[11]),   0],
                    [(hands_z1[0]-hands_z2[12]),   0],
                    [(hands_z1[0]-hands_z2[13]),   0],
                    [(hands_z1[0]-hands_z2[14]),   0],
                    [(hands_z1[0]-hands_z2[15]),   0],
                    [(hands_z1[0]-hands_z2[16]),   0],
                    [(hands_z1[0]-hands_z2[17]),   0],
                    [(hands_z1[0]-hands_z2[18]),   0],
                    [(hands_z1[0]-hands_z2[19]),   0],
                    [(hands_z1[0]-hands_z2[20]),   0]
                ]


            ## hands_relation
            if len(hand_Right) > 0 and len(hand_Left) > 0 and hand_relation:
                ### hand Right
                hands_xR = list(map(lambda a: (a['x']), hand_Right))
                hands_yR = list(map(lambda a: (a['y']), hand_Right))
                hands_zR = list(map(lambda a: (a['z']), hand_Right))
                ### hand Left
                hands_xL = list(map(lambda a: (a['x']), hand_Left))
                hands_yL = list(map(lambda a: (a['y']), hand_Left))
                hands_zL = list(map(lambda a: (a['z']), hand_Left))

                points_hand_diffX = [
                    #Between
                    #diff-between wirst
                    [(hands_xR[0]-hands_xL[0]),    0],
                    #diff-between TIP
                    [(hands_xR[4]-hands_xL[4]),    4], [(hands_xR[8]-hands_xL[8]),    8], [(hands_xR[12]-hands_xL[12]), 12],  [(hands_xR[16]-hands_xL[16]), 16],  [(hands_xR[20]-hands_xL[20]), 20],
                    #diff-between IP-DIP
                    [(hands_xR[3]-hands_xL[3]),    3], [(hands_xR[7]-hands_xL[7]),    7], [(hands_xR[11]-hands_xL[11]), 11],  [(hands_xR[15]-hands_xL[15]), 15],  [(hands_xR[19]-hands_xL[19]), 19],
                    #diff-between MCP-PIP
                    [(hands_xR[2]-hands_xL[2]),    2], [(hands_xR[6]-hands_xL[6]),    6], [(hands_xR[10]-hands_xL[10]), 10],  [(hands_xR[14]-hands_xL[14]), 14],  [(hands_xR[18]-hands_xL[18]), 18],
                    #diff-between CMC-MCP
                    [(hands_xR[1]-hands_xL[1]),    1], [(hands_xR[5]-hands_xL[5]),    5], [(hands_xR[9]-hands_xL[9]),    9],  [(hands_xR[13]-hands_xL[13]), 13],  [(hands_xR[17]-hands_xL[17]), 17]
                ]

                points_hand_diffY = [
                    #Between
                    #diff-between wirst
                    [(hands_yR[0]-hands_yL[0]),    0],
                    #diff-between TIP
                    [(hands_yR[4]-hands_yL[4]),    4], [(hands_yR[8]-hands_yL[8]),    8], [(hands_yR[12]-hands_yL[12]), 12],  [(hands_yR[16]-hands_yL[16]), 16],  [(hands_yR[20]-hands_yL[20]), 20],
                    #diff-between IP
                    [(hands_yR[3]-hands_yL[3]),    3], [(hands_yR[7]-hands_yL[7]),    7], [(hands_yR[11]-hands_yL[11]), 11],  [(hands_yR[15]-hands_yL[15]), 15],  [(hands_yR[19]-hands_yL[19]), 19],
                    #diff-between MCP
                    [(hands_yR[2]-hands_yL[2]),    2], [(hands_yR[6]-hands_yL[6]),    6], [(hands_yR[10]-hands_yL[10]), 10],  [(hands_yR[14]-hands_yL[14]), 14],  [(hands_yR[18]-hands_yL[18]), 18],
                    #diff-between CMC
                    [(hands_yR[1]-hands_yL[1]),    1], [(hands_yR[5]-hands_yL[5]),    5], [(hands_yR[9]-hands_yL[9]),    9],  [(hands_yR[13]-hands_yL[13]), 13],  [(hands_yR[17]-hands_yL[17]), 17]
                ]

                points_hand_diffZ = [
                    #Between
                    #diff-between wirst
                    [(hands_zR[0]-hands_zL[0]),    0],
                    #diff-between TIP
                    [(hands_zR[4]-hands_zL[4]),    4], [(hands_zR[8]-hands_zL[8]),    8], [(hands_zR[12]-hands_zL[12]), 12],  [(hands_zR[16]-hands_zL[16]), 16],  [(hands_zR[20]-hands_zL[20]), 20],
                    #diff-between IP
                    [(hands_zR[3]-hands_zL[3]),    3], [(hands_zR[7]-hands_zL[7]),    7], [(hands_zR[11]-hands_zL[11]), 11],  [(hands_zR[15]-hands_zL[15]), 15],  [(hands_zR[19]-hands_zL[19]), 19],
                    #diff-between MCP
                    [(hands_zR[2]-hands_zL[2]),    2], [(hands_zR[6]-hands_zL[6]),    6], [(hands_zR[10]-hands_zL[10]), 10],  [(hands_zR[14]-hands_zL[14]), 14],  [(hands_zR[18]-hands_zL[18]), 18],
                    #diff-between CMC
                    [(hands_zR[1]-hands_zL[1]),    1], [(hands_zR[5]-hands_zL[5]),    5], [(hands_zR[9]-hands_zL[9]),    9],  [(hands_zR[13]-hands_zL[13]), 13],  [(hands_zR[17]-hands_zL[17]), 17]
                ]

            #body
            if body_relation and len(points_body)>0:

                body_x = list(map(lambda a: (a['x']), points_body))
                body_y = list(map(lambda a: (a['y']), points_body))
                body_z = list(map(lambda a: (a['z']), points_body))

                ## relation into same hands
                if len(hand_Right) > 0:
                    
                    points_body_XRight = [
                        #muñeca-codo
                        [(body_x[16]-body_x[14]),   16], 
                        #codo-hombro
                        [(body_x[14]-body_x[12]),   14],
                        #hombro-muñeca
                        [(body_x[12]-body_x[16]),   12]

                    ]

                    points_body_YRight = [
                        #muñeca-codo
                        [(body_y[16]-body_y[14]),   16], 
                        #codo-hombro
                        [(body_y[14]-body_y[12]),   14],
                        #hombro-muñeca
                        [(body_y[12]-body_y[16]),   12]
                    ]

                    points_body_ZRight = [
                        #muñeca-codo
                        [(body_z[16]-body_z[14]),   16], 
                        #codo-hombro
                        [(body_z[14]-body_z[12]),   14],
                        #hombro-muñeca
                        [(body_z[14]-body_z[12]),   14]
                    ]

                if len(hand_Left) > 0:
                    
                    points_body_XLeft = [
                        #muñeca-codo
                        [(body_x[15]-body_x[13]),   15], 
                        #codo-hombro
                        [(body_x[13]-body_x[11]),   13],
                        #hombro-muñeca
                        [(body_x[11]-body_x[15]),   11]
                    ]

                    points_body_YLeft = [
                        #muñeca-codo
                        [(body_y[15]-body_y[13]),   15], 
                        #codo-hombro
                        [(body_y[13]-body_y[11]),   13],
                        #hombro-muñeca
                        [(body_y[11]-body_y[15]),   11]
                    ]

                    points_body_ZLeft = [
                        #muñeca-codo
                        [(body_z[15]-body_z[13]),   15], 
                        #codo-hombro
                        [(body_z[13]-body_z[11]),   13],
                        #hombro-muñeca
                        [(body_z[11]-body_z[15]),   11]
                    ]

                ### relation into differents hands
                if hand_diff_relation:
                    if len(hand_Right) > 0:
                        
                        points_body_relation_diffXRight = [
                            [(body_x[16]-body_x[11]),   11], [(body_x[16]-body_x[13]),   13], [(body_x[16]-body_x[15]),   15]
                        ]

                        points_body_relation_diffYRight = [
                            [(body_y[16]-body_y[11]),   11], [(body_y[16]-body_y[13]),   13], [(body_y[16]-body_y[15]),   15]
                        ]

                        points_body_relation_diffZRight = [
                            [(body_z[16]-body_z[11]),   11], [(body_z[16]-body_z[13]),   13], [(body_z[16]-body_z[15]),   15]
                        ]

                    if len(hand_Left) > 0:
                        
                        points_body_relation_diffXLeft = [
                            [(body_x[15]-body_x[12]),   12], [(body_x[13]-body_x[11]),   13], [(body_x[13]-body_x[11]),   13]
                        ]

                        points_body_relation_diffYLeft = [
                            [(body_y[15]-body_y[12]),   12], [(body_y[13]-body_y[11]),   13], [(body_y[13]-body_y[11]),   13]
                        ]

                        points_body_relation_diffZLeft = [
                            [(body_z[15]-body_z[12]),   12], [(body_z[13]-body_z[11]),   13], [(body_z[13]-body_z[11]),   13]
                        ]

                ## hand_relation
                if len(hand_Left) > 0 and len(hand_Right) > 0 and hand_relation:
                    points_body_diffX = [
                        [(body_x[16]-body_x[15]),   16], [(body_x[14]-body_x[13]),   14],
                        [(body_x[15]-body_x[16]),   15], [(body_x[13]-body_x[14]),   13]
                    ]

                    points_body_diffY = [
                        [(body_y[16]-body_y[15]),   16], [(body_y[14]-body_y[13]),   14],
                        [(body_y[15]-body_y[16]),   15], [(body_y[13]-body_y[14]),   13]
                    ]

                    points_body_diffZ = [
                        [(body_z[16]-body_z[15]),   16], [(body_z[14]-body_z[13]),   14],
                        [(body_z[15]-body_z[16]),   15], [(body_z[13]-body_z[14]),   13]
                    ]

            #body-face  
            if (body_relation and face_relation) and len(points_body)>0:

                body_x = list(map(lambda a: (a['x']), points_body))
                body_y = list(map(lambda a: (a['y']), points_body))
                body_z = list(map(lambda a: (a['z']), points_body))

                ## relation into same hands
                if len(hand_Left) > 0:

                    points_body_face_XLeft = [
                        #ear
                        [(body_x[15]-body_x[7]),  15], 
                        #eye
                        [(body_x[15]-body_x[2]),  15],
                        #nose
                        [(body_x[15]-body_x[0]),  15],
                        #mouth
                        [(body_x[15]-body_x[9]),  15]
                    ]

                    points_body_face_YLeft = [
                        #eye
                        [(body_y[15]-body_y[7]),  15], 
                        #ear
                        [(body_y[15]-body_y[2]),  15], 
                        #nose
                        [(body_y[15]-body_y[0]),  15],
                        #mouth
                        [(body_y[15]-body_y[9]),  15]
                    ]

                    points_body_face_ZLeft = [
                        #ear
                        [(body_z[15]-body_z[7]),  15], 
                        #eye
                        [(body_z[15]-body_z[2]),  15], 
                        #nose
                        [(body_z[15]-body_z[0]),  15],
                        #mouth
                        [(body_z[15]-body_z[9]),  15]
                    ]

                if len(hand_Right) > 0:

                    points_body_face_XRight = [
                        #ear
                        [(body_x[16]-body_x[8]),  16], 
                        #eye
                        [(body_x[16]-body_x[5]),  16],
                        #nose
                        [(body_x[16]-body_x[0]),  16],
                        #mouth
                        [(body_x[16]-body_x[10]), 16]
                    ]
                    
                    points_body_face_YRight = [
                        #ear
                        [(body_y[16]-body_y[8]),  16], 
                        #eye
                        [(body_y[16]-body_y[5]),  16],
                        #nose
                        [(body_y[16]-body_y[0]),  16],
                        #mouth
                        [(body_y[16]-body_y[10]), 16]
                    ]
                    
                    points_body_face_ZRight = [
                        #ear
                        [(body_z[16]-body_z[8]),  16], 
                        #eye
                        [(body_z[16]-body_z[5]),  16],
                        #nose
                        [(body_z[16]-body_z[0]),  16],
                        #mouth
                        [(body_z[16]-body_z[10]), 16]
                    ]

                ## relation into different hands
                if hand_diff_relation:
                    if len(hand_Left) > 0:
                        points_body_face_relation_diffXLeft = [
                            #ear
                            [(body_x[15]-body_x[8]),  16], 
                            #eye
                            [(body_x[15]-body_x[5]),  16],
                            #nose
                            [(body_x[15]-body_x[0]),  16],
                            #mouth
                            [(body_x[15]-body_x[10]), 16]
                        ]
                        
                        points_body_face_relation_diffYLeft = [
                            #ear
                            [(body_y[15]-body_y[8]),  16], 
                            #eye
                            [(body_y[15]-body_y[5]),  16],
                            #nose
                            [(body_y[15]-body_y[0]),  16],
                            #mouth
                            [(body_y[15]-body_y[10]), 16]
                        ]
                        
                        points_body_face_relation_diffZLeft = [
                            #ear
                            [(body_z[15]-body_z[8]),  16], 
                            #eye
                            [(body_z[15]-body_z[5]),  16],
                            #nose
                            [(body_z[15]-body_z[0]),  16],
                            #mouth
                            [(body_z[15]-body_z[10]), 16]
                        ]

                    if len(hand_Right) > 0:

                        points_body_face_relation_diffXRight = [
                            #ear
                            [(body_x[16]-body_x[7]),  15], 
                            #eye
                            [(body_x[15]-body_x[2]),  15],
                            #nose
                            [(body_x[16]-body_x[0]),  15],
                            #mouth
                            [(body_x[16]-body_x[9]),  15]
                        ]

                        points_body_face_relation_diffYRight = [
                            #ear
                            [(body_y[16]-body_y[7]),  15], 
                            #eye
                            [(body_y[15]-body_y[2]),  15], 
                            #nose
                            [(body_y[16]-body_y[0]),  15],
                            #mouth
                            [(body_y[16]-body_y[9]),  15]
                        ]

                        points_body_face_relation_diffZRight = [
                            #ear
                            [(body_z[16]-body_z[7]),  15], 
                            #eye
                            [(body_z[15]-body_z[2]),  15], 
                            #nose
                            [(body_z[16]-body_z[0]),  15],
                            #mouth
                            [(body_z[16]-body_z[9]),  15]
                        ]

            #face 
            if (face_relation) and not body_relation and len(points_body)>0:

                #Body
                body_x = list(map(lambda a: (a['x']), points_body))
                body_y = list(map(lambda a: (a['y']), points_body))
                body_z = list(map(lambda a: (a['z']), points_body))
                
                ## relation into same hands
                if len(hand_Left)>0:
                    #Left Hand
                    hands_x = list(map(lambda a: (a['x']), hand_Left))
                    hands_y = list(map(lambda a: (a['y']), hand_Left))
                    hands_z = list(map(lambda a: (a['z']), hand_Left))
                    ## Left Hand
                    points_face_XLeft = [
                        #thumb 
                        [(hands_x[4]-body_x[2]),     4],   [(hands_x[4]-body_x[0]),     4],   [(hands_x[4]-body_x[7]),     4],   [(hands_x[4]-body_x[9]),     4],
                        [(hands_x[3]-body_x[2]),     3],   [(hands_x[3]-body_x[0]),     3],   [(hands_x[3]-body_x[7]),     3],   [(hands_x[3]-body_x[9]),     3],
                        [(hands_x[2]-body_x[2]),     2],   [(hands_x[2]-body_x[0]),     2],   [(hands_x[2]-body_x[7]),     2],   [(hands_x[2]-body_x[9]),     2],
                        [(hands_x[1]-body_x[2]),     1],   [(hands_x[1]-body_x[0]),     1],   [(hands_x[1]-body_x[7]),     1],   [(hands_x[1]-body_x[9]),     1],
                        #wirst
                        [(hands_x[0]-body_x[2]),     0],   [(hands_x[0]-body_x[0]),     0],   [(hands_x[0]-body_x[7]),     0],   [(hands_x[0]-body_x[9]),     0],
                        #index
                        [(hands_x[8]-body_x[2]),     8],   [(hands_x[8]-body_x[0]),     8],   [(hands_x[8]-body_x[7]),     8],   [(hands_x[8]-body_x[9]),     8],
                        [(hands_x[7]-body_x[2]),     7],   [(hands_x[7]-body_x[0]),     7],   [(hands_x[7]-body_x[7]),     7],   [(hands_x[7]-body_x[9]),     7],
                        [(hands_x[6]-body_x[2]),     6],   [(hands_x[6]-body_x[0]),     6],   [(hands_x[6]-body_x[7]),     6],   [(hands_x[6]-body_x[9]),     6],
                        [(hands_x[5]-body_x[2]),     5],   [(hands_x[5]-body_x[0]),     5],   [(hands_x[5]-body_x[7]),     5],   [(hands_x[5]-body_x[9]),     5],
                        #middle
                        [(hands_x[12]-body_x[2]),   12],   [(hands_x[12]-body_x[0]),   12],   [(hands_x[12]-body_x[7]),   12],   [(hands_x[12]-body_x[9]),   12],
                        [(hands_x[11]-body_x[2]),   11],   [(hands_x[11]-body_x[0]),   11],   [(hands_x[11]-body_x[7]),   11],   [(hands_x[11]-body_x[9]),   11],
                        [(hands_x[10]-body_x[2]),   10],   [(hands_x[10]-body_x[0]),   10],   [(hands_x[10]-body_x[7]),   10],   [(hands_x[10]-body_x[9]),   10],
                        [(hands_x[9]-body_x[2]),     9],   [(hands_x[9]-body_x[0]),     9],   [(hands_x[9]-body_x[7]),     9],   [(hands_x[9]-body_x[9]),     9],
                        #ring
                        [(hands_x[16]-body_x[2]),   16],   [(hands_x[16]-body_x[0]),   16],   [(hands_x[16]-body_x[7]),   16],   [(hands_x[16]-body_x[9]),   16],
                        [(hands_x[15]-body_x[2]),   15],   [(hands_x[15]-body_x[0]),   15],   [(hands_x[15]-body_x[7]),   15],   [(hands_x[15]-body_x[9]),   15],
                        [(hands_x[14]-body_x[2]),   14],   [(hands_x[14]-body_x[0]),   14],   [(hands_x[14]-body_x[7]),   14],   [(hands_x[14]-body_x[9]),   14],
                        [(hands_x[13]-body_x[2]),   13],   [(hands_x[13]-body_x[0]),   13],   [(hands_x[13]-body_x[7]),   13],   [(hands_x[13]-body_x[9]),   13],
                        #pinky
                        [(hands_x[20]-body_x[2]),   20],   [(hands_x[20]-body_x[0]),   20],   [(hands_x[20]-body_x[7]),   20],   [(hands_x[20]-body_x[9]),   20],
                        [(hands_x[19]-body_x[2]),   19],   [(hands_x[19]-body_x[0]),   19],   [(hands_x[19]-body_x[7]),   19],   [(hands_x[19]-body_x[9]),   19],
                        [(hands_x[18]-body_x[2]),   18],   [(hands_x[18]-body_x[0]),   18],   [(hands_x[18]-body_x[7]),   18],   [(hands_x[18]-body_x[9]),   18],
                        [(hands_x[17]-body_x[2]),   17],   [(hands_x[17]-body_x[0]),   17],   [(hands_x[17]-body_x[7]),   17],   [(hands_x[17]-body_x[9]),   17]
                    ]
                    
                    points_face_YLeft = [
                        #thumb 
                        [(hands_y[4]-body_y[2]),     4],   [(hands_y[4]-body_y[0]),     4],   [(hands_y[4]-body_y[7]),     4],   [(hands_y[4]-body_y[9]),     4],
                        [(hands_y[3]-body_y[2]),     3],   [(hands_y[3]-body_y[0]),     3],   [(hands_y[3]-body_y[7]),     3],   [(hands_y[3]-body_y[9]),     3],
                        [(hands_y[2]-body_y[2]),     2],   [(hands_y[2]-body_y[0]),     2],   [(hands_y[2]-body_y[7]),     2],   [(hands_y[2]-body_y[9]),     2],
                        [(hands_y[1]-body_y[2]),     1],   [(hands_y[1]-body_y[0]),     1],   [(hands_y[1]-body_y[7]),     1],   [(hands_y[1]-body_y[9]),     1],
                        #wirst
                        [(hands_y[0]-body_y[2]),     0],   [(hands_y[0]-body_y[0]),     0],   [(hands_y[0]-body_y[7]),     0],   [(hands_y[0]-body_y[9]),     0],
                        #index
                        [(hands_y[8]-body_y[2]),     8],   [(hands_y[8]-body_y[0]),     8],   [(hands_y[8]-body_y[7]),     8],   [(hands_y[8]-body_y[9]),     8],
                        [(hands_y[7]-body_y[2]),     7],   [(hands_y[7]-body_y[0]),     7],   [(hands_y[7]-body_y[7]),     7],   [(hands_y[7]-body_y[9]),     7],
                        [(hands_y[6]-body_y[2]),     6],   [(hands_y[6]-body_y[0]),     6],   [(hands_y[6]-body_y[7]),     6],   [(hands_y[6]-body_y[9]),     6],
                        [(hands_y[5]-body_y[2]),     5],   [(hands_y[5]-body_y[0]),     5],   [(hands_y[5]-body_y[7]),     5],   [(hands_y[5]-body_y[9]),     5],
                        #middle
                        [(hands_y[12]-body_y[2]),   12],   [(hands_y[12]-body_y[0]),   12],   [(hands_y[12]-body_y[7]),   12],   [(hands_y[12]-body_y[9]),   12],
                        [(hands_y[11]-body_y[2]),   11],   [(hands_y[11]-body_y[0]),   11],   [(hands_y[11]-body_y[7]),   11],   [(hands_y[11]-body_y[9]),   11],
                        [(hands_y[10]-body_y[2]),   10],   [(hands_y[10]-body_y[0]),   10],   [(hands_y[10]-body_y[7]),   10],   [(hands_y[10]-body_y[9]),   10],
                        [(hands_y[9]-body_y[2]),     9],   [(hands_y[9]-body_y[0]),     9],   [(hands_y[9]-body_y[7]),     9],   [(hands_y[9]-body_y[9]),     9],
                        #ring
                        [(hands_y[16]-body_y[2]),   16],   [(hands_y[16]-body_y[0]),   16],   [(hands_y[16]-body_y[7]),   16],   [(hands_y[16]-body_y[9]),   16],
                        [(hands_y[15]-body_y[2]),   15],   [(hands_y[15]-body_y[0]),   15],   [(hands_y[15]-body_y[7]),   15],   [(hands_y[15]-body_y[9]),   15],
                        [(hands_y[14]-body_y[2]),   14],   [(hands_y[14]-body_y[0]),   14],   [(hands_y[14]-body_y[7]),   14],   [(hands_y[14]-body_y[9]),   14],
                        [(hands_y[13]-body_y[2]),   13],   [(hands_y[13]-body_y[0]),   13],   [(hands_y[13]-body_y[7]),   13],   [(hands_y[13]-body_y[9]),   13],
                        #pinky
                        [(hands_y[20]-body_y[2]),   20],   [(hands_y[20]-body_y[0]),   20],   [(hands_y[20]-body_y[7]),   20],   [(hands_y[20]-body_y[9]),   20],
                        [(hands_y[19]-body_y[2]),   19],   [(hands_y[19]-body_y[0]),   19],   [(hands_y[19]-body_y[7]),   19],   [(hands_y[19]-body_y[9]),   19],
                        [(hands_y[18]-body_y[2]),   18],   [(hands_y[18]-body_y[0]),   18],   [(hands_y[18]-body_y[7]),   18],   [(hands_y[18]-body_y[9]),   18],
                        [(hands_y[17]-body_y[2]),   17],   [(hands_y[17]-body_y[0]),   17],   [(hands_y[17]-body_y[7]),   17],   [(hands_y[17]-body_y[9]),   17]
                    ]
                    
                    points_face_ZLeft = [
                        #thumb 
                        [(hands_z[4]-body_z[2]),     4],   [(hands_z[4]-body_z[0]),     4],   [(hands_z[4]-body_z[7]),     4],   [(hands_z[4]-body_z[9]),     4],
                        [(hands_z[3]-body_z[2]),     3],   [(hands_z[3]-body_z[0]),     3],   [(hands_z[3]-body_z[7]),     3],   [(hands_z[3]-body_z[9]),     3],
                        [(hands_z[2]-body_z[2]),     2],   [(hands_z[2]-body_z[0]),     2],   [(hands_z[2]-body_z[7]),     2],   [(hands_z[2]-body_z[9]),     2],
                        [(hands_z[1]-body_z[2]),     1],   [(hands_z[1]-body_z[0]),     1],   [(hands_z[1]-body_z[7]),     1],   [(hands_z[1]-body_z[9]),     1],
                        #wirst
                        [(hands_z[0]-body_z[2]),     0],   [(hands_z[0]-body_z[0]),     0],   [(hands_z[0]-body_z[7]),     0],   [(hands_z[0]-body_z[9]),     0],
                        #index
                        [(hands_z[8]-body_z[2]),     8],   [(hands_z[8]-body_z[0]),     8],   [(hands_z[8]-body_z[7]),     8],   [(hands_z[8]-body_z[9]),     8],
                        [(hands_z[7]-body_z[2]),     7],   [(hands_z[7]-body_z[0]),     7],   [(hands_z[7]-body_z[7]),     7],   [(hands_z[7]-body_z[9]),     7],
                        [(hands_z[6]-body_z[2]),     6],   [(hands_z[6]-body_z[0]),     6],   [(hands_z[6]-body_z[7]),     6],   [(hands_z[6]-body_z[9]),     6],
                        [(hands_z[5]-body_z[2]),     5],   [(hands_z[5]-body_z[0]),     5],   [(hands_z[5]-body_z[7]),     5],   [(hands_z[5]-body_z[9]),     5],
                        #middle
                        [(hands_z[12]-body_z[2]),   12],   [(hands_z[12]-body_z[0]),   12],   [(hands_z[12]-body_z[7]),   12],   [(hands_z[12]-body_z[9]),   12],
                        [(hands_z[11]-body_z[2]),   11],   [(hands_z[11]-body_z[0]),   11],   [(hands_z[11]-body_z[7]),   11],   [(hands_z[11]-body_z[9]),   11],
                        [(hands_z[10]-body_z[2]),   10],   [(hands_z[10]-body_z[0]),   10],   [(hands_z[10]-body_z[7]),   10],   [(hands_z[10]-body_z[9]),   10],
                        [(hands_z[9]-body_z[2]),     9],   [(hands_z[9]-body_z[0]),     9],   [(hands_z[9]-body_z[7]),     9],   [(hands_z[9]-body_z[9]),     9],
                        #ring
                        [(hands_z[16]-body_z[2]),   16],   [(hands_z[16]-body_z[0]),   16],   [(hands_z[16]-body_z[7]),   16],   [(hands_z[16]-body_z[9]),   16],
                        [(hands_z[15]-body_z[2]),   15],   [(hands_z[15]-body_z[0]),   15],   [(hands_z[15]-body_z[7]),   15],   [(hands_z[15]-body_z[9]),   15],
                        [(hands_z[14]-body_z[2]),   14],   [(hands_z[14]-body_z[0]),   14],   [(hands_z[14]-body_z[7]),   14],   [(hands_z[14]-body_z[9]),   14],
                        [(hands_z[13]-body_z[2]),   13],   [(hands_z[13]-body_z[0]),   13],   [(hands_z[13]-body_z[7]),   13],   [(hands_z[13]-body_z[9]),   13],
                        #pinky
                        [(hands_z[20]-body_z[2]),   20],   [(hands_z[20]-body_z[0]),   20],   [(hands_z[20]-body_z[7]),   20],   [(hands_z[20]-body_z[9]),   20],
                        [(hands_z[19]-body_z[2]),   19],   [(hands_z[19]-body_z[0]),   19],   [(hands_z[19]-body_z[7]),   19],   [(hands_z[19]-body_z[9]),   19],
                        [(hands_z[18]-body_z[2]),   18],   [(hands_z[18]-body_z[0]),   18],   [(hands_z[18]-body_z[7]),   18],   [(hands_z[18]-body_z[9]),   18],
                        [(hands_z[17]-body_z[2]),   17],   [(hands_z[17]-body_z[0]),   17],   [(hands_z[17]-body_z[7]),   17],   [(hands_z[17]-body_z[9]),   17]
                    ]
                    
                if len(hand_Right)>0:
                    #Right Hand
                    hands_x = list(map(lambda a: (a['x']), hand_Right))
                    hands_y = list(map(lambda a: (a['y']), hand_Right))
                    hands_z = list(map(lambda a: (a['z']), hand_Right))
                    #Right Hand
                    points_face_XRight = [
                        #thumb 
                        [(hands_x[4]-body_x[5]),     4],   [(hands_x[4]-body_x[0]),     4],   [(hands_x[4]-body_x[8]),     4],   [(hands_x[4]-body_x[10]),    4],
                        [(hands_x[3]-body_x[5]),     3],   [(hands_x[3]-body_x[0]),     3],   [(hands_x[3]-body_x[8]),     3],   [(hands_x[3]-body_x[10]),    3],
                        [(hands_x[2]-body_x[5]),     2],   [(hands_x[2]-body_x[0]),     2],   [(hands_x[2]-body_x[8]),     2],   [(hands_x[2]-body_x[10]),    2],
                        [(hands_x[1]-body_x[5]),     1],   [(hands_x[1]-body_x[0]),     1],   [(hands_x[1]-body_x[8]),     1],   [(hands_x[1]-body_x[10]),    1],
                        #wirst
                        [(hands_x[0]-body_x[5]),     0],   [(hands_x[0]-body_x[0]),     0],   [(hands_x[0]-body_x[8]),     0],   [(hands_x[0]-body_x[10]),    0],
                        #index
                        [(hands_x[8]-body_x[5]),     8],   [(hands_x[8]-body_x[0]),     8],   [(hands_x[8]-body_x[8]),     8],   [(hands_x[8]-body_x[10]),    8],
                        [(hands_x[7]-body_x[5]),     7],   [(hands_x[7]-body_x[0]),     7],   [(hands_x[7]-body_x[8]),     7],   [(hands_x[7]-body_x[10]),    7],
                        [(hands_x[6]-body_x[5]),     6],   [(hands_x[6]-body_x[0]),     6],   [(hands_x[6]-body_x[8]),     6],   [(hands_x[6]-body_x[10]),    6],
                        [(hands_x[5]-body_x[5]),     5],   [(hands_x[5]-body_x[0]),     5],   [(hands_x[5]-body_x[8]),     5],   [(hands_x[5]-body_x[10]),    5],
                        #middle
                        [(hands_x[12]-body_x[5]),   12],   [(hands_x[12]-body_x[0]),   12],   [(hands_x[12]-body_x[8]),   12],   [(hands_x[12]-body_x[10]),  12],
                        [(hands_x[11]-body_x[5]),   11],   [(hands_x[11]-body_x[0]),   11],   [(hands_x[11]-body_x[8]),   11],   [(hands_x[11]-body_x[10]),  11],
                        [(hands_x[10]-body_x[5]),   10],   [(hands_x[10]-body_x[0]),   10],   [(hands_x[10]-body_x[8]),   10],   [(hands_x[10]-body_x[10]),  10],
                        [(hands_x[9]-body_x[5]),     9],   [(hands_x[9]-body_x[0]),     9],   [(hands_x[9]-body_x[8]),     9],   [(hands_x[9]-body_x[10]),    9],
                        #ring
                        [(hands_x[16]-body_x[5]),   16],   [(hands_x[16]-body_x[0]),   16],   [(hands_x[16]-body_x[8]),   16],   [(hands_x[16]-body_x[10]),  16],
                        [(hands_x[15]-body_x[5]),   15],   [(hands_x[15]-body_x[0]),   15],   [(hands_x[15]-body_x[8]),   15],   [(hands_x[15]-body_x[10]),  15],
                        [(hands_x[14]-body_x[5]),   14],   [(hands_x[14]-body_x[0]),   14],   [(hands_x[14]-body_x[8]),   14],   [(hands_x[14]-body_x[10]),  14],
                        [(hands_x[13]-body_x[5]),   13],   [(hands_x[13]-body_x[0]),   13],   [(hands_x[13]-body_x[8]),   13],   [(hands_x[13]-body_x[10]),  13],
                        #pinky
                        [(hands_x[20]-body_x[5]),   20],   [(hands_x[20]-body_x[0]),   20],   [(hands_x[20]-body_x[8]),   20],   [(hands_x[20]-body_x[10]),  20],
                        [(hands_x[19]-body_x[5]),   19],   [(hands_x[19]-body_x[0]),   19],   [(hands_x[19]-body_x[8]),   19],   [(hands_x[19]-body_x[10]),  19],
                        [(hands_x[18]-body_x[5]),   18],   [(hands_x[18]-body_x[0]),   18],   [(hands_x[18]-body_x[8]),   18],   [(hands_x[18]-body_x[10]),  18],
                        [(hands_x[17]-body_x[5]),   17],   [(hands_x[17]-body_x[0]),   17],   [(hands_x[17]-body_x[8]),   17],   [(hands_x[17]-body_x[10]),  17]
                    ]
                    
                    points_face_YRight = [
                        #thumb 
                        [(hands_y[4]-body_y[5]),     4],   [(hands_y[4]-body_y[0]),     4],   [(hands_y[4]-body_y[8]),     4],   [(hands_y[4]-body_y[10]),    4],
                        [(hands_y[3]-body_y[5]),     3],   [(hands_y[3]-body_y[0]),     3],   [(hands_y[3]-body_y[8]),     3],   [(hands_y[3]-body_y[10]),    3],
                        [(hands_y[2]-body_y[5]),     2],   [(hands_y[2]-body_y[0]),     2],   [(hands_y[2]-body_y[8]),     2],   [(hands_y[2]-body_y[10]),    2],
                        [(hands_y[1]-body_y[5]),     1],   [(hands_y[1]-body_y[0]),     1],   [(hands_y[1]-body_y[8]),     1],   [(hands_y[1]-body_y[10]),    1],
                        #wirst
                        [(hands_y[0]-body_y[5]),     0],   [(hands_y[0]-body_y[0]),     0],   [(hands_y[0]-body_y[8]),     0],   [(hands_y[0]-body_y[10]),    0],
                        #index
                        [(hands_y[8]-body_y[5]),     8],   [(hands_y[8]-body_y[0]),     8],   [(hands_y[8]-body_y[8]),     8],   [(hands_y[8]-body_y[10]),    8],
                        [(hands_y[7]-body_y[5]),     7],   [(hands_y[7]-body_y[0]),     7],   [(hands_y[7]-body_y[8]),     7],   [(hands_y[7]-body_y[10]),    7],
                        [(hands_y[6]-body_y[5]),     6],   [(hands_y[6]-body_y[0]),     6],   [(hands_y[6]-body_y[8]),     6],   [(hands_y[6]-body_y[10]),    6],
                        [(hands_y[5]-body_y[5]),     5],   [(hands_y[5]-body_y[0]),     5],   [(hands_y[5]-body_y[8]),     5],   [(hands_y[5]-body_y[10]),    5],
                        #middle
                        [(hands_y[12]-body_y[5]),   12],   [(hands_y[12]-body_y[0]),   12],   [(hands_y[12]-body_y[8]),   12],   [(hands_y[12]-body_y[10]),  12],
                        [(hands_y[11]-body_y[5]),   11],   [(hands_y[11]-body_y[0]),   11],   [(hands_y[11]-body_y[8]),   11],   [(hands_y[11]-body_y[10]),  11],
                        [(hands_y[10]-body_y[5]),   10],   [(hands_y[10]-body_y[0]),   10],   [(hands_y[10]-body_y[8]),   10],   [(hands_y[10]-body_y[10]),  10],
                        [(hands_y[9]-body_y[5]),     9],   [(hands_y[9]-body_y[0]),     9],   [(hands_y[9]-body_y[8]),     9],   [(hands_y[9]-body_y[10]),    9],
                        #ring
                        [(hands_y[16]-body_y[5]),   16],   [(hands_y[16]-body_y[0]),   16],   [(hands_y[16]-body_y[8]),   16],   [(hands_y[16]-body_y[10]),  16],
                        [(hands_y[15]-body_y[5]),   15],   [(hands_y[15]-body_y[0]),   15],   [(hands_y[15]-body_y[8]),   15],   [(hands_y[15]-body_y[10]),  15],
                        [(hands_y[14]-body_y[5]),   14],   [(hands_y[14]-body_y[0]),   14],   [(hands_y[14]-body_y[8]),   14],   [(hands_y[14]-body_y[10]),  14],
                        [(hands_y[13]-body_y[5]),   13],   [(hands_y[13]-body_y[0]),   13],   [(hands_y[13]-body_y[8]),   13],   [(hands_y[13]-body_y[10]),  13],
                        #pinky
                        [(hands_y[20]-body_y[5]),   20],   [(hands_y[20]-body_y[0]),   20],   [(hands_y[20]-body_y[8]),   20],   [(hands_y[20]-body_y[10]),  20],
                        [(hands_y[19]-body_y[5]),   19],   [(hands_y[19]-body_y[0]),   19],   [(hands_y[19]-body_y[8]),   19],   [(hands_y[19]-body_y[10]),  19],
                        [(hands_y[18]-body_y[5]),   18],   [(hands_y[18]-body_y[0]),   18],   [(hands_y[18]-body_y[8]),   18],   [(hands_y[18]-body_y[10]),  18],
                        [(hands_y[17]-body_y[5]),   17],   [(hands_y[17]-body_y[0]),   17],   [(hands_y[17]-body_y[8]),   17],   [(hands_y[17]-body_y[10]),  17]
                    ]
                    
                    points_face_ZRight = [
                        #thumb 
                        [(hands_z[4]-body_z[5]),     4],   [(hands_z[4]-body_z[0]),     4],   [(hands_z[4]-body_z[8]),     4],   [(hands_z[4]-body_z[10]),    4],
                        [(hands_z[3]-body_z[5]),     3],   [(hands_z[3]-body_z[0]),     3],   [(hands_z[3]-body_z[8]),     3],   [(hands_z[3]-body_z[10]),    3],
                        [(hands_z[2]-body_z[5]),     2],   [(hands_z[2]-body_z[0]),     2],   [(hands_z[2]-body_z[8]),     2],   [(hands_z[2]-body_z[10]),    2],
                        [(hands_z[1]-body_z[5]),     1],   [(hands_z[1]-body_z[0]),     1],   [(hands_z[1]-body_z[8]),     1],   [(hands_z[1]-body_z[10]),    1],
                        #wirst
                        [(hands_z[0]-body_z[5]),     0],   [(hands_z[0]-body_z[0]),     0],   [(hands_z[0]-body_z[8]),     0],   [(hands_z[0]-body_z[10]),    0],
                        #index
                        [(hands_z[8]-body_z[5]),     8],   [(hands_z[8]-body_z[0]),     8],   [(hands_z[8]-body_z[8]),     8],   [(hands_z[8]-body_z[10]),    8],
                        [(hands_z[7]-body_z[5]),     7],   [(hands_z[7]-body_z[0]),     7],   [(hands_z[7]-body_z[8]),     7],   [(hands_z[7]-body_z[10]),    7],
                        [(hands_z[6]-body_z[5]),     6],   [(hands_z[6]-body_z[0]),     6],   [(hands_z[6]-body_z[8]),     6],   [(hands_z[6]-body_z[10]),    6],
                        [(hands_z[5]-body_z[5]),     5],   [(hands_z[5]-body_z[0]),     5],   [(hands_z[5]-body_z[8]),     5],   [(hands_z[5]-body_z[10]),    5],
                        #middle
                        [(hands_z[12]-body_z[5]),   12],   [(hands_z[12]-body_z[0]),   12],   [(hands_z[12]-body_z[8]),   12],   [(hands_z[12]-body_z[10]),  12],
                        [(hands_z[11]-body_z[5]),   11],   [(hands_z[11]-body_z[0]),   11],   [(hands_z[11]-body_z[8]),   11],   [(hands_z[11]-body_z[10]),  11],
                        [(hands_z[10]-body_z[5]),   10],   [(hands_z[10]-body_z[0]),   10],   [(hands_z[10]-body_z[8]),   10],   [(hands_z[10]-body_z[10]),  10],
                        [(hands_z[9]-body_z[5]),     9],   [(hands_z[9]-body_z[0]),     9],   [(hands_z[9]-body_z[8]),     9],   [(hands_z[9]-body_z[10]),    9],
                        #ring
                        [(hands_z[16]-body_z[5]),   16],   [(hands_z[16]-body_z[0]),   16],   [(hands_z[16]-body_z[8]),   16],   [(hands_z[16]-body_z[10]),  16],
                        [(hands_z[15]-body_z[5]),   15],   [(hands_z[15]-body_z[0]),   15],   [(hands_z[15]-body_z[8]),   15],   [(hands_z[15]-body_z[10]),  15],
                        [(hands_z[14]-body_z[5]),   14],   [(hands_z[14]-body_z[0]),   14],   [(hands_z[14]-body_z[8]),   14],   [(hands_z[14]-body_z[10]),  14],
                        [(hands_z[13]-body_z[5]),   13],   [(hands_z[13]-body_z[0]),   13],   [(hands_z[13]-body_z[8]),   13],   [(hands_z[13]-body_z[10]),  13],
                        #pinky
                        [(hands_z[20]-body_z[5]),   20],   [(hands_z[20]-body_z[0]),   20],   [(hands_z[20]-body_z[8]),   20],   [(hands_z[20]-body_z[10]),  20],
                        [(hands_z[19]-body_z[5]),   19],   [(hands_z[19]-body_z[0]),   19],   [(hands_z[19]-body_z[8]),   19],   [(hands_z[19]-body_z[10]),  19],
                        [(hands_z[18]-body_z[5]),   18],   [(hands_z[18]-body_z[0]),   18],   [(hands_z[18]-body_z[8]),   18],   [(hands_z[18]-body_z[10]),  18],
                        [(hands_z[17]-body_z[5]),   17],   [(hands_z[17]-body_z[0]),   17],   [(hands_z[17]-body_z[8]),   17],   [(hands_z[17]-body_z[10]),  17]
                    ]
                
                ## relation into diff hands
                if hand_diff_relation:
                    if len(hand_Left) > 0:
                        #Left Hand
                        hands_x = list(map(lambda a: (a['x']), hand_Left))
                        hands_y = list(map(lambda a: (a['y']), hand_Left))
                        hands_z = list(map(lambda a: (a['z']), hand_Left))
                        ## Left Hand
                        points_face_relation_diffXLeft = [
                            #thumb 
                            [(hands_x[4]-body_x[5]),     4],   [(hands_x[4]-body_x[0]),     4],   [(hands_x[4]-body_x[8]),     4],   [(hands_x[4]-body_x[10]),    4],
                            [(hands_x[3]-body_x[5]),     3],   [(hands_x[3]-body_x[0]),     3],   [(hands_x[3]-body_x[8]),     3],   [(hands_x[3]-body_x[10]),    3],
                            [(hands_x[2]-body_x[5]),     2],   [(hands_x[2]-body_x[0]),     2],   [(hands_x[2]-body_x[8]),     2],   [(hands_x[2]-body_x[10]),    2],
                            [(hands_x[1]-body_x[5]),     1],   [(hands_x[1]-body_x[0]),     1],   [(hands_x[1]-body_x[8]),     1],   [(hands_x[1]-body_x[10]),    1],
                            #wirst
                            [(hands_x[0]-body_x[5]),     0],   [(hands_x[0]-body_x[0]),     0],   [(hands_x[0]-body_x[8]),     0],   [(hands_x[0]-body_x[10]),    0],
                            #index
                            [(hands_x[8]-body_x[5]),     8],   [(hands_x[8]-body_x[0]),     8],   [(hands_x[8]-body_x[8]),     8],   [(hands_x[8]-body_x[10]),    8],
                            [(hands_x[7]-body_x[5]),     7],   [(hands_x[7]-body_x[0]),     7],   [(hands_x[7]-body_x[8]),     7],   [(hands_x[7]-body_x[10]),    7],
                            [(hands_x[6]-body_x[5]),     6],   [(hands_x[6]-body_x[0]),     6],   [(hands_x[6]-body_x[8]),     6],   [(hands_x[6]-body_x[10]),    6],
                            [(hands_x[5]-body_x[5]),     5],   [(hands_x[5]-body_x[0]),     5],   [(hands_x[5]-body_x[8]),     5],   [(hands_x[5]-body_x[10]),    5],
                            #middle
                            [(hands_x[12]-body_x[5]),   12],   [(hands_x[12]-body_x[0]),   12],   [(hands_x[12]-body_x[8]),   12],   [(hands_x[12]-body_x[10]),  12],
                            [(hands_x[11]-body_x[5]),   11],   [(hands_x[11]-body_x[0]),   11],   [(hands_x[11]-body_x[8]),   11],   [(hands_x[11]-body_x[10]),  11],
                            [(hands_x[10]-body_x[5]),   10],   [(hands_x[10]-body_x[0]),   10],   [(hands_x[10]-body_x[8]),   10],   [(hands_x[10]-body_x[10]),  10],
                            [(hands_x[9]-body_x[5]),     9],   [(hands_x[9]-body_x[0]),     9],   [(hands_x[9]-body_x[8]),     9],   [(hands_x[9]-body_x[10]),    9],
                            #ring
                            [(hands_x[16]-body_x[5]),   16],   [(hands_x[16]-body_x[0]),   16],   [(hands_x[16]-body_x[8]),   16],   [(hands_x[16]-body_x[10]),  16],
                            [(hands_x[15]-body_x[5]),   15],   [(hands_x[15]-body_x[0]),   15],   [(hands_x[15]-body_x[8]),   15],   [(hands_x[15]-body_x[10]),  15],
                            [(hands_x[14]-body_x[5]),   14],   [(hands_x[14]-body_x[0]),   14],   [(hands_x[14]-body_x[8]),   14],   [(hands_x[14]-body_x[10]),  14],
                            [(hands_x[13]-body_x[5]),   13],   [(hands_x[13]-body_x[0]),   13],   [(hands_x[13]-body_x[8]),   13],   [(hands_x[13]-body_x[10]),  13],
                            #pinky
                            [(hands_x[20]-body_x[5]),   20],   [(hands_x[20]-body_x[0]),   20],   [(hands_x[20]-body_x[8]),   20],   [(hands_x[20]-body_x[10]),  20],
                            [(hands_x[19]-body_x[5]),   19],   [(hands_x[19]-body_x[0]),   19],   [(hands_x[19]-body_x[8]),   19],   [(hands_x[19]-body_x[10]),  19],
                            [(hands_x[18]-body_x[5]),   18],   [(hands_x[18]-body_x[0]),   18],   [(hands_x[18]-body_x[8]),   18],   [(hands_x[18]-body_x[10]),  18],
                            [(hands_x[17]-body_x[5]),   17],   [(hands_x[17]-body_x[0]),   17],   [(hands_x[17]-body_x[8]),   17],   [(hands_x[17]-body_x[10]),  17]
                        ]
                        
                        points_face_relation_diffYLeft = [
                            #thumb 
                            [(hands_y[4]-body_y[5]),     4],   [(hands_y[4]-body_y[0]),     4],   [(hands_y[4]-body_y[8]),     4],   [(hands_y[4]-body_y[10]),    4],
                            [(hands_y[3]-body_y[5]),     3],   [(hands_y[3]-body_y[0]),     3],   [(hands_y[3]-body_y[8]),     3],   [(hands_y[3]-body_y[10]),    3],
                            [(hands_y[2]-body_y[5]),     2],   [(hands_y[2]-body_y[0]),     2],   [(hands_y[2]-body_y[8]),     2],   [(hands_y[2]-body_y[10]),    2],
                            [(hands_y[1]-body_y[5]),     1],   [(hands_y[1]-body_y[0]),     1],   [(hands_y[1]-body_y[8]),     1],   [(hands_y[1]-body_y[10]),    1],
                            #wirst
                            [(hands_y[0]-body_y[5]),     0],   [(hands_y[0]-body_y[0]),     0],   [(hands_y[0]-body_y[8]),     0],   [(hands_y[0]-body_y[10]),    0],
                            #index
                            [(hands_y[8]-body_y[5]),     8],   [(hands_y[8]-body_y[0]),     8],   [(hands_y[8]-body_y[8]),     8],   [(hands_y[8]-body_y[10]),    8],
                            [(hands_y[7]-body_y[5]),     7],   [(hands_y[7]-body_y[0]),     7],   [(hands_y[7]-body_y[8]),     7],   [(hands_y[7]-body_y[10]),    7],
                            [(hands_y[6]-body_y[5]),     6],   [(hands_y[6]-body_y[0]),     6],   [(hands_y[6]-body_y[8]),     6],   [(hands_y[6]-body_y[10]),    6],
                            [(hands_y[5]-body_y[5]),     5],   [(hands_y[5]-body_y[0]),     5],   [(hands_y[5]-body_y[8]),     5],   [(hands_y[5]-body_y[10]),    5],
                            #middle
                            [(hands_y[12]-body_y[5]),   12],   [(hands_y[12]-body_y[0]),   12],   [(hands_y[12]-body_y[8]),   12],   [(hands_y[12]-body_y[10]),  12],
                            [(hands_y[11]-body_y[5]),   11],   [(hands_y[11]-body_y[0]),   11],   [(hands_y[11]-body_y[8]),   11],   [(hands_y[11]-body_y[10]),  11],
                            [(hands_y[10]-body_y[5]),   10],   [(hands_y[10]-body_y[0]),   10],   [(hands_y[10]-body_y[8]),   10],   [(hands_y[10]-body_y[10]),  10],
                            [(hands_y[9]-body_y[5]),     9],   [(hands_y[9]-body_y[0]),     9],   [(hands_y[9]-body_y[8]),     9],   [(hands_y[9]-body_y[10]),    9],
                            #ring
                            [(hands_y[16]-body_y[5]),   16],   [(hands_y[16]-body_y[0]),   16],   [(hands_y[16]-body_y[8]),   16],   [(hands_y[16]-body_y[10]),  16],
                            [(hands_y[15]-body_y[5]),   15],   [(hands_y[15]-body_y[0]),   15],   [(hands_y[15]-body_y[8]),   15],   [(hands_y[15]-body_y[10]),  15],
                            [(hands_y[14]-body_y[5]),   14],   [(hands_y[14]-body_y[0]),   14],   [(hands_y[14]-body_y[8]),   14],   [(hands_y[14]-body_y[10]),  14],
                            [(hands_y[13]-body_y[5]),   13],   [(hands_y[13]-body_y[0]),   13],   [(hands_y[13]-body_y[8]),   13],   [(hands_y[13]-body_y[10]),  13],
                            #pinky
                            [(hands_y[20]-body_y[5]),   20],   [(hands_y[20]-body_y[0]),   20],   [(hands_y[20]-body_y[8]),   20],   [(hands_y[20]-body_y[10]),  20],
                            [(hands_y[19]-body_y[5]),   19],   [(hands_y[19]-body_y[0]),   19],   [(hands_y[19]-body_y[8]),   19],   [(hands_y[19]-body_y[10]),  19],
                            [(hands_y[18]-body_y[5]),   18],   [(hands_y[18]-body_y[0]),   18],   [(hands_y[18]-body_y[8]),   18],   [(hands_y[18]-body_y[10]),  18],
                            [(hands_y[17]-body_y[5]),   17],   [(hands_y[17]-body_y[0]),   17],   [(hands_y[17]-body_y[8]),   17],   [(hands_y[17]-body_y[10]),  17]
                        ]
                        
                        points_face_relation_diffZLeft = [
                            #thumb 
                            [(hands_z[4]-body_z[5]),     4],   [(hands_z[4]-body_z[0]),     4],   [(hands_z[4]-body_z[8]),     4],   [(hands_z[4]-body_z[10]),    4],
                            [(hands_z[3]-body_z[5]),     3],   [(hands_z[3]-body_z[0]),     3],   [(hands_z[3]-body_z[8]),     3],   [(hands_z[3]-body_z[10]),    3],
                            [(hands_z[2]-body_z[5]),     2],   [(hands_z[2]-body_z[0]),     2],   [(hands_z[2]-body_z[8]),     2],   [(hands_z[2]-body_z[10]),    2],
                            [(hands_z[1]-body_z[5]),     1],   [(hands_z[1]-body_z[0]),     1],   [(hands_z[1]-body_z[8]),     1],   [(hands_z[1]-body_z[10]),    1],
                            #wirst
                            [(hands_z[0]-body_z[5]),     0],   [(hands_z[0]-body_z[0]),     0],   [(hands_z[0]-body_z[8]),     0],   [(hands_z[0]-body_z[10]),    0],
                            #index
                            [(hands_z[8]-body_z[5]),     8],   [(hands_z[8]-body_z[0]),     8],   [(hands_z[8]-body_z[8]),     8],   [(hands_z[8]-body_z[10]),    8],
                            [(hands_z[7]-body_z[5]),     7],   [(hands_z[7]-body_z[0]),     7],   [(hands_z[7]-body_z[8]),     7],   [(hands_z[7]-body_z[10]),    7],
                            [(hands_z[6]-body_z[5]),     6],   [(hands_z[6]-body_z[0]),     6],   [(hands_z[6]-body_z[8]),     6],   [(hands_z[6]-body_z[10]),    6],
                            [(hands_z[5]-body_z[5]),     5],   [(hands_z[5]-body_z[0]),     5],   [(hands_z[5]-body_z[8]),     5],   [(hands_z[5]-body_z[10]),    5],
                            #middle
                            [(hands_z[12]-body_z[5]),   12],   [(hands_z[12]-body_z[0]),   12],   [(hands_z[12]-body_z[8]),   12],   [(hands_z[12]-body_z[10]),  12],
                            [(hands_z[11]-body_z[5]),   11],   [(hands_z[11]-body_z[0]),   11],   [(hands_z[11]-body_z[8]),   11],   [(hands_z[11]-body_z[10]),  11],
                            [(hands_z[10]-body_z[5]),   10],   [(hands_z[10]-body_z[0]),   10],   [(hands_z[10]-body_z[8]),   10],   [(hands_z[10]-body_z[10]),  10],
                            [(hands_z[9]-body_z[5]),     9],   [(hands_z[9]-body_z[0]),     9],   [(hands_z[9]-body_z[8]),     9],   [(hands_z[9]-body_z[10]),    9],
                            #ring
                            [(hands_z[16]-body_z[5]),   16],   [(hands_z[16]-body_z[0]),   16],   [(hands_z[16]-body_z[8]),   16],   [(hands_z[16]-body_z[10]),  16],
                            [(hands_z[15]-body_z[5]),   15],   [(hands_z[15]-body_z[0]),   15],   [(hands_z[15]-body_z[8]),   15],   [(hands_z[15]-body_z[10]),  15],
                            [(hands_z[14]-body_z[5]),   14],   [(hands_z[14]-body_z[0]),   14],   [(hands_z[14]-body_z[8]),   14],   [(hands_z[14]-body_z[10]),  14],
                            [(hands_z[13]-body_z[5]),   13],   [(hands_z[13]-body_z[0]),   13],   [(hands_z[13]-body_z[8]),   13],   [(hands_z[13]-body_z[10]),  13],
                            #pinky
                            [(hands_z[20]-body_z[5]),   20],   [(hands_z[20]-body_z[0]),   20],   [(hands_z[20]-body_z[8]),   20],   [(hands_z[20]-body_z[10]),  20],
                            [(hands_z[19]-body_z[5]),   19],   [(hands_z[19]-body_z[0]),   19],   [(hands_z[19]-body_z[8]),   19],   [(hands_z[19]-body_z[10]),  19],
                            [(hands_z[18]-body_z[5]),   18],   [(hands_z[18]-body_z[0]),   18],   [(hands_z[18]-body_z[8]),   18],   [(hands_z[18]-body_z[10]),  18],
                            [(hands_z[17]-body_z[5]),   17],   [(hands_z[17]-body_z[0]),   17],   [(hands_z[17]-body_z[8]),   17],   [(hands_z[17]-body_z[10]),  17]
                        ]
                    
                    if len(hand_Right) > 0:
                        #Right Hand
                        hands_x = list(map(lambda a: (a['x']), hand_Right))
                        hands_y = list(map(lambda a: (a['y']), hand_Right))
                        hands_z = list(map(lambda a: (a['z']), hand_Right))
                        #Right Hand
                        points_face_relation_diffXRight = [
                            #thumb 
                            [(hands_x[4]-body_x[2]),     4],   [(hands_x[4]-body_x[0]),     4],   [(hands_x[4]-body_x[7]),     4],   [(hands_x[4]-body_x[9]),     4],
                            [(hands_x[3]-body_x[2]),     3],   [(hands_x[3]-body_x[0]),     3],   [(hands_x[3]-body_x[7]),     3],   [(hands_x[3]-body_x[9]),     3],
                            [(hands_x[2]-body_x[2]),     2],   [(hands_x[2]-body_x[0]),     2],   [(hands_x[2]-body_x[7]),     2],   [(hands_x[2]-body_x[9]),     2],
                            [(hands_x[1]-body_x[2]),     1],   [(hands_x[1]-body_x[0]),     1],   [(hands_x[1]-body_x[7]),     1],   [(hands_x[1]-body_x[9]),     1],
                            #wirst
                            [(hands_x[0]-body_x[2]),     0],   [(hands_x[0]-body_x[0]),     0],   [(hands_x[0]-body_x[7]),     0],   [(hands_x[0]-body_x[9]),     0],
                            #index
                            [(hands_x[8]-body_x[2]),     8],   [(hands_x[8]-body_x[0]),     8],   [(hands_x[8]-body_x[7]),     8],   [(hands_x[8]-body_x[9]),     8],
                            [(hands_x[7]-body_x[2]),     7],   [(hands_x[7]-body_x[0]),     7],   [(hands_x[7]-body_x[7]),     7],   [(hands_x[7]-body_x[9]),     7],
                            [(hands_x[6]-body_x[2]),     6],   [(hands_x[6]-body_x[0]),     6],   [(hands_x[6]-body_x[7]),     6],   [(hands_x[6]-body_x[9]),     6],
                            [(hands_x[5]-body_x[2]),     5],   [(hands_x[5]-body_x[0]),     5],   [(hands_x[5]-body_x[7]),     5],   [(hands_x[5]-body_x[9]),     5],
                            #middle
                            [(hands_x[12]-body_x[2]),   12],   [(hands_x[12]-body_x[0]),   12],   [(hands_x[12]-body_x[7]),   12],   [(hands_x[12]-body_x[9]),   12],
                            [(hands_x[11]-body_x[2]),   11],   [(hands_x[11]-body_x[0]),   11],   [(hands_x[11]-body_x[7]),   11],   [(hands_x[11]-body_x[9]),   11],
                            [(hands_x[10]-body_x[2]),   10],   [(hands_x[10]-body_x[0]),   10],   [(hands_x[10]-body_x[7]),   10],   [(hands_x[10]-body_x[9]),   10],
                            [(hands_x[9]-body_x[2]),     9],   [(hands_x[9]-body_x[0]),     9],   [(hands_x[9]-body_x[7]),     9],   [(hands_x[9]-body_x[9]),     9],
                            #ring
                            [(hands_x[16]-body_x[2]),   16],   [(hands_x[16]-body_x[0]),   16],   [(hands_x[16]-body_x[7]),   16],   [(hands_x[16]-body_x[9]),   16],
                            [(hands_x[15]-body_x[2]),   15],   [(hands_x[15]-body_x[0]),   15],   [(hands_x[15]-body_x[7]),   15],   [(hands_x[15]-body_x[9]),   15],
                            [(hands_x[14]-body_x[2]),   14],   [(hands_x[14]-body_x[0]),   14],   [(hands_x[14]-body_x[7]),   14],   [(hands_x[14]-body_x[9]),   14],
                            [(hands_x[13]-body_x[2]),   13],   [(hands_x[13]-body_x[0]),   13],   [(hands_x[13]-body_x[7]),   13],   [(hands_x[13]-body_x[9]),   13],
                            #pinky
                            [(hands_x[20]-body_x[2]),   20],   [(hands_x[20]-body_x[0]),   20],   [(hands_x[20]-body_x[7]),   20],   [(hands_x[20]-body_x[9]),   20],
                            [(hands_x[19]-body_x[2]),   19],   [(hands_x[19]-body_x[0]),   19],   [(hands_x[19]-body_x[7]),   19],   [(hands_x[19]-body_x[9]),   19],
                            [(hands_x[18]-body_x[2]),   18],   [(hands_x[18]-body_x[0]),   18],   [(hands_x[18]-body_x[7]),   18],   [(hands_x[18]-body_x[9]),   18],
                            [(hands_x[17]-body_x[2]),   17],   [(hands_x[17]-body_x[0]),   17],   [(hands_x[17]-body_x[7]),   17],   [(hands_x[17]-body_x[9]),   17]
                        ]
                        
                        points_face_relation_diffYRight = [
                            #thumb 
                            [(hands_y[4]-body_y[2]),     4],   [(hands_y[4]-body_y[0]),     4],   [(hands_y[4]-body_y[7]),     4],   [(hands_y[4]-body_y[9]),     4],
                            [(hands_y[3]-body_y[2]),     3],   [(hands_y[3]-body_y[0]),     3],   [(hands_y[3]-body_y[7]),     3],   [(hands_y[3]-body_y[9]),     3],
                            [(hands_y[2]-body_y[2]),     2],   [(hands_y[2]-body_y[0]),     2],   [(hands_y[2]-body_y[7]),     2],   [(hands_y[2]-body_y[9]),     2],
                            [(hands_y[1]-body_y[2]),     1],   [(hands_y[1]-body_y[0]),     1],   [(hands_y[1]-body_y[7]),     1],   [(hands_y[1]-body_y[9]),     1],
                            #wirst
                            [(hands_y[0]-body_y[2]),     0],   [(hands_y[0]-body_y[0]),     0],   [(hands_y[0]-body_y[7]),     0],   [(hands_y[0]-body_y[9]),     0],
                            #index
                            [(hands_y[8]-body_y[2]),     8],   [(hands_y[8]-body_y[0]),     8],   [(hands_y[8]-body_y[7]),     8],   [(hands_y[8]-body_y[9]),     8],
                            [(hands_y[7]-body_y[2]),     7],   [(hands_y[7]-body_y[0]),     7],   [(hands_y[7]-body_y[7]),     7],   [(hands_y[7]-body_y[9]),     7],
                            [(hands_y[6]-body_y[2]),     6],   [(hands_y[6]-body_y[0]),     6],   [(hands_y[6]-body_y[7]),     6],   [(hands_y[6]-body_y[9]),     6],
                            [(hands_y[5]-body_y[2]),     5],   [(hands_y[5]-body_y[0]),     5],   [(hands_y[5]-body_y[7]),     5],   [(hands_y[5]-body_y[9]),     5],
                            #middle
                            [(hands_y[12]-body_y[2]),   12],   [(hands_y[12]-body_y[0]),   12],   [(hands_y[12]-body_y[7]),   12],   [(hands_y[12]-body_y[9]),   12],
                            [(hands_y[11]-body_y[2]),   11],   [(hands_y[11]-body_y[0]),   11],   [(hands_y[11]-body_y[7]),   11],   [(hands_y[11]-body_y[9]),   11],
                            [(hands_y[10]-body_y[2]),   10],   [(hands_y[10]-body_y[0]),   10],   [(hands_y[10]-body_y[7]),   10],   [(hands_y[10]-body_y[9]),   10],
                            [(hands_y[9]-body_y[2]),     9],   [(hands_y[9]-body_y[0]),     9],   [(hands_y[9]-body_y[7]),     9],   [(hands_y[9]-body_y[9]),     9],
                            #ring
                            [(hands_y[16]-body_y[2]),   16],   [(hands_y[16]-body_y[0]),   16],   [(hands_y[16]-body_y[7]),   16],   [(hands_y[16]-body_y[9]),   16],
                            [(hands_y[15]-body_y[2]),   15],   [(hands_y[15]-body_y[0]),   15],   [(hands_y[15]-body_y[7]),   15],   [(hands_y[15]-body_y[9]),   15],
                            [(hands_y[14]-body_y[2]),   14],   [(hands_y[14]-body_y[0]),   14],   [(hands_y[14]-body_y[7]),   14],   [(hands_y[14]-body_y[9]),   14],
                            [(hands_y[13]-body_y[2]),   13],   [(hands_y[13]-body_y[0]),   13],   [(hands_y[13]-body_y[7]),   13],   [(hands_y[13]-body_y[9]),   13],
                            #pinky
                            [(hands_y[20]-body_y[2]),   20],   [(hands_y[20]-body_y[0]),   20],   [(hands_y[20]-body_y[7]),   20],   [(hands_y[20]-body_y[9]),   20],
                            [(hands_y[19]-body_y[2]),   19],   [(hands_y[19]-body_y[0]),   19],   [(hands_y[19]-body_y[7]),   19],   [(hands_y[19]-body_y[9]),   19],
                            [(hands_y[18]-body_y[2]),   18],   [(hands_y[18]-body_y[0]),   18],   [(hands_y[18]-body_y[7]),   18],   [(hands_y[18]-body_y[9]),   18],
                            [(hands_y[17]-body_y[2]),   17],   [(hands_y[17]-body_y[0]),   17],   [(hands_y[17]-body_y[7]),   17],   [(hands_y[17]-body_y[9]),   17]
                        ]
                        
                        points_face_relation_diffZRight = [
                            #thumb 
                            [(hands_z[4]-body_z[2]),     4],   [(hands_z[4]-body_z[0]),     4],   [(hands_z[4]-body_z[7]),     4],   [(hands_z[4]-body_z[9]),     4],
                            [(hands_z[3]-body_z[2]),     3],   [(hands_z[3]-body_z[0]),     3],   [(hands_z[3]-body_z[7]),     3],   [(hands_z[3]-body_z[9]),     3],
                            [(hands_z[2]-body_z[2]),     2],   [(hands_z[2]-body_z[0]),     2],   [(hands_z[2]-body_z[7]),     2],   [(hands_z[2]-body_z[9]),     2],
                            [(hands_z[1]-body_z[2]),     1],   [(hands_z[1]-body_z[0]),     1],   [(hands_z[1]-body_z[7]),     1],   [(hands_z[1]-body_z[9]),     1],
                            #wirst
                            [(hands_z[0]-body_z[2]),     0],   [(hands_z[0]-body_z[0]),     0],   [(hands_z[0]-body_z[7]),     0],   [(hands_z[0]-body_z[9]),     0],
                            #index
                            [(hands_z[8]-body_z[2]),     8],   [(hands_z[8]-body_z[0]),     8],   [(hands_z[8]-body_z[7]),     8],   [(hands_z[8]-body_z[9]),     8],
                            [(hands_z[7]-body_z[2]),     7],   [(hands_z[7]-body_z[0]),     7],   [(hands_z[7]-body_z[7]),     7],   [(hands_z[7]-body_z[9]),     7],
                            [(hands_z[6]-body_z[2]),     6],   [(hands_z[6]-body_z[0]),     6],   [(hands_z[6]-body_z[7]),     6],   [(hands_z[6]-body_z[9]),     6],
                            [(hands_z[5]-body_z[2]),     5],   [(hands_z[5]-body_z[0]),     5],   [(hands_z[5]-body_z[7]),     5],   [(hands_z[5]-body_z[9]),     5],
                            #middle
                            [(hands_z[12]-body_z[2]),   12],   [(hands_z[12]-body_z[0]),   12],   [(hands_z[12]-body_z[7]),   12],   [(hands_z[12]-body_z[9]),   12],
                            [(hands_z[11]-body_z[2]),   11],   [(hands_z[11]-body_z[0]),   11],   [(hands_z[11]-body_z[7]),   11],   [(hands_z[11]-body_z[9]),   11],
                            [(hands_z[10]-body_z[2]),   10],   [(hands_z[10]-body_z[0]),   10],   [(hands_z[10]-body_z[7]),   10],   [(hands_z[10]-body_z[9]),   10],
                            [(hands_z[9]-body_z[2]),     9],   [(hands_z[9]-body_z[0]),     9],   [(hands_z[9]-body_z[7]),     9],   [(hands_z[9]-body_z[9]),     9],
                            #ring
                            [(hands_z[16]-body_z[2]),   16],   [(hands_z[16]-body_z[0]),   16],   [(hands_z[16]-body_z[7]),   16],   [(hands_z[16]-body_z[9]),   16],
                            [(hands_z[15]-body_z[2]),   15],   [(hands_z[15]-body_z[0]),   15],   [(hands_z[15]-body_z[7]),   15],   [(hands_z[15]-body_z[9]),   15],
                            [(hands_z[14]-body_z[2]),   14],   [(hands_z[14]-body_z[0]),   14],   [(hands_z[14]-body_z[7]),   14],   [(hands_z[14]-body_z[9]),   14],
                            [(hands_z[13]-body_z[2]),   13],   [(hands_z[13]-body_z[0]),   13],   [(hands_z[13]-body_z[7]),   13],   [(hands_z[13]-body_z[9]),   13],
                            #pinky
                            [(hands_z[20]-body_z[2]),   20],   [(hands_z[20]-body_z[0]),   20],   [(hands_z[20]-body_z[7]),   20],   [(hands_z[20]-body_z[9]),   20],
                            [(hands_z[19]-body_z[2]),   19],   [(hands_z[19]-body_z[0]),   19],   [(hands_z[19]-body_z[7]),   19],   [(hands_z[19]-body_z[9]),   19],
                            [(hands_z[18]-body_z[2]),   18],   [(hands_z[18]-body_z[0]),   18],   [(hands_z[18]-body_z[7]),   18],   [(hands_z[18]-body_z[9]),   18],
                            [(hands_z[17]-body_z[2]),   17],   [(hands_z[17]-body_z[0]),   17],   [(hands_z[17]-body_z[7]),   17],   [(hands_z[17]-body_z[9]),   17]
                        ]             

            #return values
            return [
                ## hands difference --> when: hand_relation
                points_hand_diffX,#0
                points_hand_diffY,#1
                points_hand_diffZ,#2
                ## hands relation  --> indepent of hand_relation, same hands
                points_hand_Right_diffX,#3
                points_hand_Right_diffY,#4
                points_hand_Right_diffZ,#5
                points_hand_Left_diffX,#6
                points_hand_Left_diffY,#7
                points_hand_Left_diffZ,#8
                ## hands relation  --> indepent of hand_relation, diff hands
                points_hand_relation_diffX,#9
                points_hand_relation_diffY,#10
                points_hand_relation_diffZ,#11
                ## body difference --> when: hand_relation
                points_body_diffX,#12
                points_body_diffY,#13
                points_body_diffZ,#14
                ## hands_body relation --> indepent of hand_relation, same hands
                points_body_XRight,#15
                points_body_YRight,#16
                points_body_ZRight,#17
                points_body_XLeft,#18
                points_body_YLeft,#19
                points_body_ZLeft,#20
                ## hands_body relation --> indepent of hand_relation, diff hands
                points_body_relation_diffXRight,#21
                points_body_relation_diffYRight,#22
                points_body_relation_diffZRight,#23
                points_body_relation_diffXLeft,#24
                points_body_relation_diffYLeft,#25
                points_body_relation_diffZLeft,#26
                ## body_face relation --> indepent of hand_relation, same hand
                points_body_face_XRight,#27
                points_body_face_YRight,#28
                points_body_face_ZRight,#29
                points_body_face_XLeft,#30
                points_body_face_YLeft,#31
                points_body_face_ZLeft,#32
                ## body_face relation --> indepent of hand_relation, diff hand
                points_body_face_relation_diffXRight,#33
                points_body_face_relation_diffYRight,#34
                points_body_face_relation_diffZRight,#35
                points_body_face_relation_diffXLeft,#36
                points_body_face_relation_diffYLeft,#37
                points_body_face_relation_diffZLeft,#38
                ## face relation  --> indepent of hand_relation, sane hand
                points_face_XRight,#39
                points_face_YRight,#40
                points_face_ZRight,#41
                points_face_XLeft,#42
                points_face_YLeft,#43
                points_face_ZLeft,#44
                ## face relation  --> indepent of hand_relation, diff hand
                points_face_relation_diffXRight,#45
                points_face_relation_diffYRight,#46
                points_face_relation_diffZRight,#47
                points_face_relation_diffXLeft,#48
                points_face_relation_diffYLeft,#49
                points_face_relation_diffZLeft#50
                
            ]

        except Exception as e:
            print("Error Ocurrido [Hand model - make_model], Mensaje: {0}".format(str(e)))
            return None
        
    def make_model_body(self, hand_Left=None, hand_Right=None, points_body=None):
        try:
            if points_body is None or hand_Left is None or hand_Right is None:
                return None
            
            points_body_RightX = []
            points_body_RightY = []
            points_body_RightZ = []
            points_body_LeftX = []
            points_body_LeftY = []
            points_body_LeftZ = []

            body_x = list(map(lambda a: (a['x']), points_body))
            body_y = list(map(lambda a: (a['y']), points_body))
            body_z = list(map(lambda a: (a['z']), points_body))

            if len(hand_Right)>0:

                points_body_RightX = [
                    [(body_x[16]-body_x[22]), 16], [(body_x[16]-body_x[18]), 16], [(body_x[16]-body_x[20]), 16],
                    [(body_x[14]-body_x[22]), 14], [(body_x[16]-body_x[14]), 16], [(body_x[16]-body_x[20]), 16],
                    [(body_x[12]-body_x[16]), 12], [(body_x[12]-body_x[14]), 12]
                ]

                points_body_RightY = [
                    [(body_y[16]-body_y[22]), 16], [(body_y[16]-body_y[18]), 16], [(body_y[16]-body_y[20]), 16],
                    [(body_y[14]-body_y[22]), 14], [(body_y[16]-body_y[14]), 16], [(body_y[16]-body_y[20]), 16],
                    [(body_y[12]-body_y[16]), 12], [(body_y[12]-body_y[14]), 12]
                ]

                points_body_RightZ = [
                    [(body_z[16]-body_z[22]), 16], [(body_z[16]-body_z[18]), 16], [(body_z[16]-body_z[20]), 16],
                    [(body_z[14]-body_z[22]), 14], [(body_z[16]-body_z[14]), 16], [(body_z[16]-body_z[20]), 16],
                    [(body_z[12]-body_z[16]), 12], [(body_z[12]-body_z[14]), 12]
                ]

            if len(hand_Left)>0:

                points_body_LeftX = [
                    [(body_x[15]-body_x[21]), 15], [(body_x[15]-body_x[17]), 15], [(body_x[15]-body_x[19]), 15],
                    [(body_x[13]-body_x[21]), 13], [(body_x[13]-body_x[17]), 13], [(body_x[13]-body_x[19]), 13],
                    [(body_x[11]-body_x[15]), 11], [(body_x[11]-body_x[13]), 11]
                ]

                points_body_LeftY = [
                    [(body_y[15]-body_y[21]), 15], [(body_y[15]-body_y[17]), 15], [(body_y[15]-body_y[19]), 15],
                    [(body_y[13]-body_y[21]), 13], [(body_y[13]-body_y[17]), 13], [(body_y[13]-body_y[19]), 13],
                    [(body_y[11]-body_y[15]), 11], [(body_y[11]-body_y[13]), 11]
                ]

                points_body_LeftZ = [
                    [(body_z[15]-body_z[21]), 15], [(body_z[15]-body_z[17]), 15], [(body_z[15]-body_z[19]), 15],
                    [(body_z[13]-body_z[21]), 13], [(body_z[13]-body_z[17]), 13], [(body_z[13]-body_z[19]), 13],
                    [(body_z[11]-body_z[15]), 11], [(body_z[11]-body_z[13]), 11]
                ]


            return [
                points_body_RightX,
                points_body_RightY,
                points_body_RightZ,
                points_body_LeftX,
                points_body_LeftY,
                points_body_LeftZ
            ]

        except Exception as e:
            print("Error Ocurrido [Hand model - make_model_body], Mensaje: {0}".format(str(e)))
            return None