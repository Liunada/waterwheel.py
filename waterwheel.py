from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakeBox
from OCC.Core.gp import gp_Pnt, gp_Ax2, gp_Dir, gp_Trsf, gp_Vec
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse
from OCC.Core.STEPControl import STEPControl_Writer, STEPControl_AsIs

# Parameters
wheel_diameter = 100  # mm
wheel_width = 30  # mm
num_blades = 12
blade_width = 5  # mm
blade_height = 30  # mm
axle_diameter = 10  # mm

# Create the main wheel body
wheel = BRepPrimAPI_MakeCylinder(wheel_diameter / 2, wheel_width).Shape()

# Create the axle hole
axle = BRepPrimAPI_MakeCylinder(axle_diameter / 2, wheel_width + 2).Shape()
wheel = BRepAlgoAPI_Cut(wheel, axle).Shape()

# Create blades and attach them to the wheel
blade_angle = 360 / num_blades
for i in range(num_blades):
    angle = blade_angle * i
    blade = BRepPrimAPI_MakeBox(blade_width, blade_height, wheel_width).Shape()
    translation = gp_Trsf()
    translation.SetTranslation(
        gp_Vec(
            (wheel_diameter / 2 - blade_width / 2) * gp_Dir(1, 0, 0),
            0,
            0
        )
    )
    blade = BRepBuilderAPI_Transform(blade, translation).Shape()
    rotation = gp_Trsf()
    rotation.SetRotation(gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1)), angle)
    blade = BRepBuilderAPI_Transform(blade, rotation).Shape()
    wheel = BRepAlgoAPI_Fuse(wheel, blade).Shape()

# Export the model to a STEP file
step_writer = STEPControl_Writer()
step_writer.Transfer(wheel, STEPControl_AsIs)
step_writer.Write("waterwheel.step")

print("Waterwheel model saved as waterwheel.step")
