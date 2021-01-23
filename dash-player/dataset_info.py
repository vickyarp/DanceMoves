
import dash_html_components as html
import dash_core_components as dcc

txt = dcc.Markdown('''
    * `PB_F/S`: ** _pas de bourre_ **, small displacement, legs and arms move concurrently
    * `PC_F/S`: ** _“pas de cheval”_ **, no spatial displacement, one leg movement
    * `RV_R_F/S`: ** _“renverse”_ **, complex step, spatial displacement with a turn on the air/jump
    * `BVT_R_F/S`: ** _“brizee vole”_ **, a series of identical small jumps with diagonal forward spatial displacement
    * `PV_R_F/S`: “pas de valse en tournant”, complex step, diagonal backward spatial displacement
    * `LD_F/S_dis`: “pique a cote”, side step, one leg always on the floor, arms move concurrently
    * `LD_F/S_small`: “tendue en arriere”, leg extends to the back, maintains floor contact
    * `LU_F/S_dis`: “pique a cote”, side step, leg up to 90° above the floor, arms move concurrently
    * `LU_F/S_big`: “arabesque”, leg up to 90° above the floor
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
    * `TB_F/S_FB`: “tour pique”, backward turn, end facing back
    * `TB_S`: “tour pique”, backward turn
    * `TF_F/S`: “tour pique”, forward turn
    * `TF_F/S`: “tour pique”, forward turn
    * `TL_F/S`: “tour pique”, leftward turn
    * `TR_F/S`: “tour pique”, rightward turn
    * `TOS_F/S`: “tour pique”, turn with no spatial displacement
    * `BJ_BK`: “brizee”, large backwards jump
    * `BJ_FT`: “brizee”, large forward jump
    * `BG_LT`: “brizee”, large leftward jump
    * `SJ_BK`: “brizee”, small backwards jump
    * `SJ_FT`: “brizee”, small forward jump
    * `SJ_LT`: “brizee”, small leftward jump
    * `SJ_RT`: “brizee”, small rightward jump
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
    * `CH`: “chasse”, big displacement, no arm movement
    * `EF`: “pas de cheval”, small jump, no displacement, no arm movement
    * `CH`: “PE: “pense”, leg upwards while torso downward, performed on the spot
    * `AR`: “arabesque”, leg upwards to 90° above the floor, performed on the spot
    * `TA`: “tendue en arriere”, leg extends to the back and remains on the floor, it is 	performed on the spot
    * `AS_L_NA/WA`: “assemble”, a small jump, leg to the side, a jump, legs meet on the air, followed by landing
    * `BA_R_NA/WA`: “ballote”, standing on pointes with a small jump on the spot, leg extension to the front, small jump extending other leg to the back
    * `CU_R_NA/WA`: “courou”, standing on pointes, very small steps moving diagonally to the front
    * `FR_R_NA/WA`: “frappe”, on the spot extension of the leg to the front and then the left side, by hitting foot on the floor
    * `SB_R_NA/WA`: “saute de basque”, movement through space by alternating legs and sliding on the floor, continuous movement
''')

txt2 = [
    html.Div(html.H5("File pose variation naming:")),
    html.Div("File names with ‘_F’ or ‘_S’ point to execution times of a given step that are of faster or slower speed, respectively."),
    html.Div("File names with ‘_WA’ or ‘_NA’ point to execution of a given step with or without arm movement, respectively. "),
    html.Div("File names with ‘_BK’,‘_FT’, ‘_LT’ or ‘_RT’ point movement to the back, front, left or right, respectively. "),
    html.Br(),
    html.Div(html.H5("Detailed encoding:")),
    html.Div(txt),
    # html.Div("PB_F/S: “pas de bourre”, small displacement, legs and arms move concurrently"),
    # html.Div("PC_F/S: “pas de cheval”, no spatial displacement, one leg movement"),
    # html.Div("RV_R_F/S: “renverse”, complex step, spatial displacement with a turn on the air/jump"),
    # html.Div("BVT_R_F/S: “brizee vole”, a series of identical small jumps with diagonal forward spatial displacement"),
    # html.Div("PV_R_F/S: “pas de valse en tournant”, complex step, diagonal backward spatial displacement"),
    # html.Div("LD_F/S_dis: “pique a cote”, side step, one leg always on the floor, arms move concurrently"),
    # html.Div("LD_F/S_small: “tendue en arriere”, leg extends to the back, maintains floor contact"),
    # html.Div("LU_F/S_dis: “pique a cote”, side step, leg up to 90° above the floor, arms move concurrently"),
    # html.Div("LU_F/S_big: “arabesque”, leg up to 90° above the floor"),
    # html.Div("BBS_F/S_BK: dancer facing backwards, large step to the back (receding movement)"),
    # html.Div("BBS_F/S_FT: dancer facing backwards, large step to the front (looming movement)"),
    # html.Div("BSS_F/S_BK: dancer facing backwards, small step to the back (receding)"),
    # html.Div("BSS_F/S_FT: dancer facing backwards, small step to the front (looming)"),
    # html.Div("BS_F/S_BK: dancer front-view, big step to the back (receding)"),
    # html.Div("SS_F/S_BK: dancer front-view, small step to the back (receding)"),
    # html.Div("BS_F/S_FT: dancer front-view, big step to the front (looming)"),
    # html.Div("SS_F/S_FT: dancer front-view, small step to the front (looming)"),
    # html.Div("SS_F/S_LT: dancer front-view, small step to the left"),
    # html.Div("BS_F/S_RT: dancer front-view, big step to the right"),
    # html.Div("SS_F/S_RT: dancer front-view, small step to the right"),
    # html.Div("TB_F/S_FB: “tour pique”, backward turn, end facing back"),
    # html.Div("TB_S: “tour pique”, backward turn"),
    # html.Div("TF_F/S: “tour pique”, forward turn"),
    # html.Div("TF_F/S: “tour pique”, forward turn"),
    # html.Div("TL_F/S: “tour pique”, leftward turn"),
    # html.Div("TR_F/S: “tour pique”, rightward turn"),
    # html.Div("TOS_F/S: “tour pique”, turn with no spatial displacement"),
    # html.Div("BJ_BK: “brizee”, large backwards jump"),
    # html.Div("BJ_FT: “brizee”, large forward jump"),
    # html.Div("BG_LT: “brizee”, large leftward jump"),
    # html.Div("SJ_BK: “brizee”, small backwards jump"),
    # html.Div("SJ_FT: “brizee”, small forward jump"),
    # html.Div("SJ_LT: “brizee”, small leftward jump"),
    # html.Div("SJ_RT: “brizee”, small rightward jump"),
    # html.Div("P1: a falling movement of the torso to the side"),
    # html.Div("P2: a turn on the spot and a falling movement of the torso"),
    # html.Div("P3: the weight shifts forward followed by a falling movement"),
    # html.Div("UP1: reaching out with the arms towards one direction but falling towards the opposite"),
    # html.Div("UP2: a turn that ends towards one direction and falling towards the opposite"),
    # html.Div("UP3: a shift of weight leads to a fall towards one direction but abruptly the arm leads the body towards another direction"),
    # html.Div("SYN_U: leg lift while sliding arms on the body"),
    # html.Div("SYN_B: seating on the floor with legs bend followed by leg slide to full stretch"),
    # html.Div("SYN_D: bend knees while sliding arms on the body"),
    # html.Div("SYN_K: stand on knee and slide other leg on the floor in a circular motion  "),
    # html.Div("SYN_R: circular movement by sliding foot on the floor while standing on the spot"),
    # html.Div("SYN_S: shifting of the weight and simulated falling by bending torso to the side, followed by a return to initial position"),
    # html.Div("CH: “chasse”, big displacement, no arm movement"),
    # html.Div("EF: “pas de cheval”, small jump, no displacement, no arm movement"),
    # html.Div("CH: “PE: “pense”, leg upwards while torso downward, performed on the spot"),
    # html.Div("AR: “arabesque”, leg upwards to 90° above the floor, performed on the spot"),
    # html.Div("TA: “tendue en arriere”, leg extends to the back and remains on the floor, it is 	performed on the spot"),
    # html.Div("AS_L_NA/WA: “assemble”, a small jump, leg to the side, a jump, legs meet on the air, followed by landing"),
    # html.Div("BA_R_NA/WA: “ballote”, standing on pointes with a small jump on the spot, leg extension to the front, small jump extending other leg to the back"),
    # html.Div("CU_R_NA/WA: “courou”, standing on pointes, very small steps moving diagonally to the front"),
    # html.Div("FR_R_NA/WA: “frappe”, on the spot extension of the leg to the front and then the left side, by hitting foot on the floor"),
    # html.Div("SB_R_NA/WA: “saute de basque”, movement through space by alternating legs and sliding on the floor, continuous movement"),
    html.Div(""),
    html.Div(""),
    html.Div(""),
]



















