
import dash_html_components as html
import dash_core_components as dcc

txt = dcc.Markdown('''
    * `PB_F/S`: ** _“pas de bourre”_ **, small displacement, legs and arms move concurrently
    * `PC_F/S`: ** _“pas de cheval”_ **, no spatial displacement, one leg movement
    * `RV_R_F/S`: ** _“renverse”_ **, complex step, spatial displacement with a turn on the air/jump
    * `BVT_R_F/S`: ** _“brizee vole”_ **, a series of identical small jumps with diagonal forward spatial displacement
    * `PV_R_F/S`: ** _“pas de valse en tournant”_ ** , complex step, diagonal backward spatial displacement
    * `LD_F/S_dis`: ** _“pique a cote”_ **, side step, one leg always on the floor, arms move concurrently
    * `LD_F/S_small`: ** _“tendue en arriere”_ **, leg extends to the back, maintains floor contact
    * `LU_F/S_dis`: ** _“pique a cote”_ **, side step, leg up to 90° above the floor, arms move concurrently
    * `LU_F/S_big`: “arabesque”_ **, leg up to 90° above the floor
    * `BBS_F/S_BK`: dancer facing backwards, large step to the back (receding movement)
    * `BBS_F/S_FT`: dancer facing backwards, large step to the front (looming movement)
    * `BSS_F/S_BK`: dancer facing backwards, small step to the back (receding)
    * `BSS_F/S_FT`: dancer facing backwards, small step to the front (looming)
    * `BS_F/S_BK`: dancer front-view, big step to the back (receding)
    * `SS_F/S_BK`: dancer front-view, small step to the back (receding)
    * `BS_F/S_FT`: dancer front-view, big step to the front (looming)
    * `SS_F/S_FT`: dancer front-view, small step to the front (looming)
    * `SS_F/S_LT`: dancer front-view, small step to the left
    * `BS_F/S_RT`: dancer front-view, big step to the right
    * `SS_F/S_RT`: dancer front-view, small step to the right
    * `TB_F/S_FB`: ** _“tour pique”_ **, backward turn, end facing back
    * `TB_S`: ** _“tour pique”_ **, backward turn
    * `TF_F/S`: ** _“tour pique”_ **, forward turn
    * `TF_F/S`: ** _“tour pique”_ **, forward turn
    * `TL_F/S`: ** _“tour pique”_ **, leftward turn
    * `TR_F/S`: ** _“tour pique”_ **, rightward turn
    * `TOS_F/S`: ** _“tour pique”_ **, turn with no spatial displacement
    * `BJ_BK`: ** _“brizee”_ **, large backwards jump
    * `BJ_FT`: ** _“brizee”_ **, large forward jump
    * `BG_LT`: ** _“brizee”_ **, large leftward jump
    * `SJ_BK`: ** _“brizee”_ **, small backwards jump
    * `SJ_FT`: ** _“brizee”_ **, small forward jump
    * `SJ_LT`: ** _“brizee”_ **, small leftward jump
    * `SJ_RT`: ** _“brizee”_ **, small rightward jump
    * `P1`: a falling movement of the torso to the side
    * `P2`: a turn on the spot and a falling movement of the torso
    * `P3`: the weight shifts forward followed by a falling movement
    * `UP1`: reaching out with the arms towards one direction but falling towards the opposite
    * `UP2`: a turn that ends towards one direction and falling towards the opposite
    * `UP3`: a shift of weight leads to a fall towards one direction but abruptly the arm leads the body towards another direction
    * `SYN_U`: leg lift while sliding arms on the body
    * `SYN_B`: seating on the floor with legs bend followed by leg slide to full stretch
    * `SYN_D`: bend knees while sliding arms on the body
    * `SYN_K`: stand on knee and slide other leg on the floor in a circular motion  
    * `SYN_R`: circular movement by sliding foot on the floor while standing on the spot
    * `SYN_S`: shifting of the weight and simulated falling by bending torso to the side, followed by a return to initial position
    * `CH`: ** _“chasse”_ **, big displacement, no arm movement
    * `EF`: ** _“pas de cheval”_ **, small jump, no displacement, no arm movement
    * `CH`: “PE: ** _“pense”_ **, leg upwards while torso downward, performed on the spot
    * `AR`: ** _“arabesque”_ **, leg upwards to 90° above the floor, performed on the spot
    * `TA`: ** _“tendue en arriere”_ **, leg extends to the back and remains on the floor, it is 	performed on the spot
    * `AS_L_NA/WA`: ** _“assemble”_ **, a small jump, leg to the side, a jump, legs meet on the air, followed by landing
    * `BA_R_NA/WA`: ** _“ballote”_ **, standing on pointes with a small jump on the spot, leg extension to the front, small jump extending other leg to the back
    * `CU_R_NA/WA`: ** _“courou”_ **, standing on pointes, very small steps moving diagonally to the front
    * `FR_R_NA/WA`: ** _“frappe”_ **, on the spot extension of the leg to the front and then the left side, by hitting foot on the floor
    * `SB_R_NA/WA`: ** _“saute de basque”_ **, movement through space by alternating legs and sliding on the floor, continuous movement
''')

txt1 = dcc.Markdown('''
   * "File names with ** _“_F”_ ** or ** _“_S”_ ** point to execution times of a given step that are of faster or slower speed, respectively.
   * "File names with ** _“_WA”_ ** or ** _“_NA”_ ** point to execution of a given step with or without arm movement, respectively.
   * "File names with ** _“_BK”_ ** ,** _“_FT”_ **, ** _“_LT”_ ** or ** _“_RT”_ ** point movement to the back, front, left or right, respectively.

''')


txt2 = [
    html.Div(html.H5("File pose variation naming:")),
    html.Div(txt1),
    html.Br(),
    html.Div(html.H5("Detailed encoding:")),
    html.Div(txt),
    html.Div(""),
    html.Div(""),
    html.Div(""),
]


txt3 = [
    html.Div(html.H5("Angle Similarity:")),
    html.Br(),
    html.Div(html.H5("Velocity Similarity:")),
    html.Div(""),
    html.Div(""),
    html.Div(""),
]











