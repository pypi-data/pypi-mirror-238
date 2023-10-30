import numpy as np 
import os
import itasca as it
it.command("python-reset-state false")


def model(R,L,List_R,scour_depth,soil_layers,prj_dir):
    layering_temp = []
    for i in soil_layers:
        layering_temp.append(i)
    layering_temp.append(soil_layers[0]-scour_depth)
    layering_temp.append(soil_layers[0]-L)
    layering_temp.sort(reverse=True)
    layering=list(set(layering_temp))
    layering.sort(key=layering_temp.index)
    
    temp = []
    for i in range(len(layering)-1):
        if layering[i] == layering[i+1]:
            temp.append(layering[i+1])
    for i in temp:
        layering.remove(i)
    # print("layerings for checking model")
    # print(layering)
    #model new#########################
    it.command("model new")
    it.command("program echo off")
    it.fish.set('R',R)
    it.fish.set('mudline',soil_layers[0])
    it.fish.set('scour_depth',scour_depth)
    it.fish.set('boundary_z',soil_layers[-1])
    #basic model
    extrusion = f'''
    extrude set select "geometry"
    extrude point create (0,0)
    extrude point create (0,{List_R[0]})
    extrude point create (0,{List_R[1]})
    extrude point create (0,{List_R[2]})
    extrude point create (0,{List_R[3]})
    extrude point create ({List_R[0]},0)
    extrude point create ({List_R[1]},0)
    extrude point create ({List_R[2]},0)
    extrude point create ({List_R[3]},0)

    extrude edge create by-points 1 2 type simple
    extrude edge create by-points 2 3 type simple
    extrude edge create by-points 3 4 type simple
    extrude edge create by-points 4 5 type simple

    extrude edge create by-points 1 6 type simple
    extrude edge create by-points 6 7 type simple
    extrude edge create by-points 7 8 type simple
    extrude edge create by-points 8 9 type simple

    extrude edge id 1 split ([0],{R/3})
    extrude edge id 5 split ({R/3},[0])
    extrude point create ({R/3},{R/3})

    extrude edge id 10 split ([0],{R})
    extrude edge id 11 split ({R},[0])
    extrude point create ([{R}*math.cos((45)/180*math.pi)],[{R}*math.sin((45)/180*math.pi)])
    ;
    extrude point create ([{List_R[0]}*math.cos((45)/180*math.pi)],[{List_R[0]}*math.sin((45)/180*math.pi)])
    extrude point create ([{List_R[1]}*math.cos((45)/180*math.pi)],[{List_R[1]}*math.sin((45)/180*math.pi)])
    extrude point create ([{List_R[2]}*math.cos((45)/180*math.pi)],[{List_R[2]}*math.sin((45)/180*math.pi)])
    extrude point create ([{List_R[3]}*math.cos((45)/180*math.pi)],[{List_R[3]}*math.sin((45)/180*math.pi)])
    ;
    extrude edge create by-points 10 12 type simple
    extrude edge create by-points 11 12 type simple
    ;
    extrude edge create by-points 13 15 type simple
    extrude edge create by-points 14 15 type simple
    extrude edge create by-points 12 15 type simple
    ;
    extrude edge create by-points 02 16 type simple
    extrude edge create by-points 06 16 type simple
    extrude edge create by-points 15 16 type simple
    ;
    extrude edge create by-points 03 17 type simple
    extrude edge create by-points 07 17 type simple
    extrude edge create by-points 16 17 type simple
    ;
    extrude edge create by-points 04 18 type simple
    extrude edge create by-points 08 18 type simple
    extrude edge create by-points 17 18 type simple
    ;
    extrude edge create by-points 05 19 type simple
    extrude edge create by-points 09 19 type simple
    extrude edge create by-points 18 19 type simple
    ;;
    extrude edge id 16 control-point add ([{R}*math.cos((22.5)/180*math.pi)],[{R}*math.sin((22.5)/180*math.pi)])
    extrude edge id 19 control-point add ([{List_R[0]}*math.cos((22.5)/180*math.pi)],[{List_R[0]}*math.sin((22.5)/180*math.pi)])
    extrude edge id 22 control-point add ([{List_R[1]}*math.cos((22.5)/180*math.pi)],[{List_R[1]}*math.sin((22.5)/180*math.pi)])
    extrude edge id 25 control-point add ([{List_R[2]}*math.cos((22.5)/180*math.pi)],[{List_R[2]}*math.sin((22.5)/180*math.pi)])
    extrude edge id 28 control-point add ([{List_R[3]}*math.cos((22.5)/180*math.pi)],[{List_R[3]}*math.sin((22.5)/180*math.pi)])
    ;
    extrude edge id 15 control-point add ([{R}*math.cos((67.5)/180*math.pi)],[{R}*math.sin((67.5)/180*math.pi)])
    extrude edge id 18 control-point add ([{List_R[0]}*math.cos((67.5)/180*math.pi)],[{List_R[0]}*math.sin((67.5)/180*math.pi)])
    extrude edge id 21 control-point add ([{List_R[1]}*math.cos((67.5)/180*math.pi)],[{List_R[1]}*math.sin((67.5)/180*math.pi)])
    extrude edge id 24 control-point add ([{List_R[2]}*math.cos((67.5)/180*math.pi)],[{List_R[2]}*math.sin((67.5)/180*math.pi)])
    extrude edge id 27 control-point add ([{List_R[3]}*math.cos((67.5)/180*math.pi)],[{List_R[3]}*math.sin((67.5)/180*math.pi)])
    ;
    extrude edge id 16 type arc
    extrude edge id 19 type arc
    extrude edge id 22 type arc
    extrude edge id 25 type arc
    extrude edge id 28 type arc
    ;
    extrude edge id 15 type arc
    extrude edge id 18 type arc
    extrude edge id 21 type arc
    extrude edge id 24 type arc
    extrude edge id 27 type arc
    ;
    extrude block create automatic
    extrude edge size 6 range id-list 1 9 11 14
    extrude edge size [int({R}/0.5)] range id-list 10
    extrude edge size [int(({List_R[0]-R})/0.5)] range id-list 13
    extrude edge size [int(({List_R[1]-List_R[0]})/0.75)] range id-list 6
    extrude edge size [int(({List_R[2]-List_R[1]})/1.00)] range id-list 7
    extrude edge size [int(({List_R[3]-List_R[2]})/1.50)] range id-list 8
    ;
    extrude segment index 1 length 0.1 size 1 group "basic" slot "Default"
    ;
    extrude set system u-axis (1,0,0) v-axis (0,1,0)
    extrude set system origin 0 0 50
    zone generate from-sketch
    '''
    it.command(extrusion)

    command = '''
    zone reflect origin 0 0 0 normal 0 1 0 merge on
    zone reflect origin 0 0 0 normal 1 0 0 merge on
    '''
    it.command(command)
    #layering
    for gp in it.gridpoint.list():
        gp.set_pos_z(gp.pos_z()-(50-layering[0]))

    command_template = ("zone copy 0 0 {} merge on range position-z {} {}")

    for i in layering:
        if i == layering[0]:
            continue
        elif i == layering[-1]:
            continue
        else:
            it.command(command_template.format(i-layering[0],layering[0],layering[1]))
        
    for gp in it.gridpoint.list():    
        for i in range(len(layering)-1):
            if round(gp.pos_z(),3) == round((layering[i]-0.1),3):
                # print(layering[i+1])
                gp.set_pos_z(layering[i+1])
      
    for z in it.zone.list():
        for i in range(len(soil_layers)-1):
            if z.pos_z() <= soil_layers[i] and z.pos_z() >= soil_layers[i+1]:
                z.set_group("soil_{}".format(i),"soil")

    for i in range(len(layering)-1):
        if layering[i]-layering[i+1] <= 0.5:
            continue
        elif layering[i]-layering[i+1] > 0.5 and layering[i]-layering[i+1] < 1.0:
            it.command("zone densify global segments 1 1 2 range position-z {} {}".format(layering[i],layering[i+1]))
        else:
            command = "zone densify global segments 1 1 {} range position-z {} {}"
            it.command(command.format((int((layering[i]-layering[i+1])*0.5)+2),layering[i],layering[i+1]))

    command = f"zone densify global segments 1 1 2 range position-z {layering[0]} {layering[0]-L-5}"
    it.command(command) 

    it.command("zone attach by-face tolerance-absolute 0.1")
    it.command(f"model save '{prj_dir}\Model'")
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("'Model' saved!")
    print("basic information for checking!")
    print(f"Diameter = {R*2}; Length = {L}")
    print(f"original soil layers: {soil_layers}")
    print(f"original model layers: {layering}")
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    #os.remove(f"{prj_dir}\zone.inp")
    