from collections import namedtuple

FACES = ['front', 'back', 'top', 'down', 'left', 'right']
AXES = ['x', 'y', 'z']

Cubelets = namedtuple('Cubelets', FACES)

Movement = namedtuple('Movement', ['face', 'is_prime'])

CubeMovement = namedtuple('CubeMovement', ['axis'])

def apply_face_rotation(cubelets, movement):
    face = movement.face
    assert face in FACES
    c = (
        apply_face_rotation(
            apply_face_rotation(cubelets, Movement(face=movement.face, is_prime=False)),
            Movement(face=movement.face, is_prime=False),
        )
        if movement.is_prime
        else cubelets
    )
    (f0, f1, f2, f3, f4, f5, f6, f7, f8) = getattr(c, 'front')
    (b0, b1, b2, b3, b4, b5, b6, b7, b8) = getattr(c, 'back')
    (t0, t1, t2, t3, t4, t5, t6, t7, t8) = getattr(c, 'top')
    (d0, d1, d2, d3, d4, d5, d6, d7, d8) = getattr(c, 'down')
    (l0, l1, l2, l3, l4, l5, l6, l7, l8) = getattr(c, 'left')
    (r0, r1, r2, r3, r4, r5, r6, r7, r8) = getattr(c, 'right')
    if face == 'front':
        return Cubelets(
            front=''.join((f6, f7, f0, f1, f2, f3, f4, f5, f8)),
            back=c.back,
            top=''.join((t0, t1, t2, l1, l2, l3, t6, t7, t8)),
            down=''.join((r6, r7, d2, d3, d4, d5, d6, r5, d8)),
            left=''.join((l0, d7, d0, d1, l4, l5, l6, l7, l8)),
            right=''.join((r0, r1, r2, r3, r4, t3, t4, t5, r8)),
        ) 
    elif face == 'back':
        return Cubelets(
            front=c.front,
            back=''.join((b6, b7, b0, b1, b2, b3, b4, b5, b8)),
            top=''.join((r2, r3, t2, t3, t4, t5, t6, r1, t8)),
            down=''.join((d0, d1, d2, l5, l6, l7, d6, d7, d8)),
            left=''.join((l0, l1, l2, l3, l4, t7, t0, t1, l8)),
            right=''.join((r0, d3, d4, d5, r4, r5, r6, r7, r8)),
        )
    elif face == 'top':
        return Cubelets(
            front=''.join((r0, r1, f2, f3, f4, f5, f6, r7, f8)),
            back=''.join((l0, l1, b2, b3, b4, b5, b6, l7, b8)),
            top=''.join((t6, t7, t0, t1, t2, t3, t4, t5, t8)),
            down=c.down,
            left=''.join((f0, f1, l2, l3, l4, l5, l6, f7, l8)),
            right=''.join((b0, b1, r2, r3, r4, r5, r6, b7, r8)),
        )
    elif face == 'down':
        return Cubelets(
            front=''.join((f0, f1, f2, l3, l4, l5, f6, f7, f8)),
            back=''.join((b0, b1, b2, r3, r4, r5, b6, b7, b8)),
            top=c.top,
            down=''.join((d6, d7, d0, d1, d2, d3, d4, d5, d8)),
            left=''.join((l0, l1, l2, b3, b4, b5, l6, l7, l8)),
            right=''.join((r0, r1, r2, f3, f4, f5, r6, r7, r8)),
        )
    elif face == 'left':
        return Cubelets(
            front=''.join((f0, f1, f2, f3, f4, t5, t6, t7, f8)),
            back=''.join((b0, d5, d6, d7, b4, b5, b6, b7, b8)),
            top=''.join((t0, t1, t2, t3, t4, b1, b2, b3, t8)),
            down=''.join((d0, d1, d2, d3, d4, f5, f6, f7, d8)),
            left=''.join((l6, l7, l0, l1, l2, l3, l4, l5, l8)),
            right=c.right,
        )
    elif face == 'right':
        return Cubelets(
            front=''.join((f0, d1, d2, d3, f4, f5, f6, f7, f8)),
            back=''.join((b0, b1, b2, b3, b4, t1, t2, t3, b8)),
            top=''.join((t0, f1, f2, f3, t4, t5, t6, t7, t8)),
            down=''.join((d0, b5, b6, b7, d4, d5, d6, d7, d8)),
            left=c.left,
            right=''.join((r6, r7, r0, r1, r2, r3, r4, r5, r8)),
        )

def apply_cube_rotation(cubelets, cube_movement): 
    axis = cube_movement.axis
    assert axis in AXES
    (f0, f1, f2, f3, f4, f5, f6, f7, f8) = getattr(c, 'front')
    (b0, b1, b2, b3, b4, b5, b6, b7, b8) = getattr(c, 'back')
    (t0, t1, t2, t3, t4, t5, t6, t7, t8) = getattr(c, 'top')
    (d0, d1, d2, d3, d4, d5, d6, d7, d8) = getattr(c, 'down')
    (l0, l1, l2, l3, l4, l5, l6, l7, l8) = getattr(c, 'left')
    (r0, r1, r2, r3, r4, r5, r6, r7, r8) = getattr(c, 'right')
    if axis == 'x':
        return Cubelets(
            front=cubelets.down,
            back=cubelets.top,
            top=cubelets.front,
            down=cubelets.back,
            left=cubelets.left,
            right=cubelets.right,
        )
    elif axis == 'y':
        return Cubelets(
            front=cubelets.front,
            back=cubelets.back,
            top=cubelets.left,
            down=cubelets.right,
            left=cubelets.down,
            right=cubelets.top,
        )
    elif axis == 'z':
        return Cubelets(
            front=cubelets.right,
            back=cubelets.left,
            top=cubelets.top,
            down=cubelets.down,
            left=cubelets.back,
            right=cubelets.front,
        ) 

def create_default_cubelets():
    return Cubelets(
        front=('W' * 9),
        back=('Y' * 9), 
        top=('O' * 9),
        down=('R' * 9),
        left=('G' * 9),
        right=('B' * 9),
    ) 

class Cube:

    def __init__(self):
        self.movement_callback = None
        self.movement_history = []
        self.reset()

    def initialize_cubelets(self):
        self.cubelets = create_default_cubelets()

    def get_cubelets(self):
        return self.cubelets

    def reset(self):
        self.initialize_cubelets()
        self.movement_history.clear()

    def rotate_face(self, movement, should_store_in_history=True):
        rotated_cubelets = apply_face_rotation(self.cubelets, movement)
        self.cubelets = rotated_cubelets
        if should_store_in_history:
            self.movement_history.append(movement)
        self.call_movement_callback()

    def rotate_cube(self, axis, is_ccw=False):
        rotated_cubelets = apply_cube_rotation(self.cubelets, CubeMovement(axis=axis))
        self.cubelets = rotated_cubelets
        self.call_movement_callback()

    def undo_face_rotation(self):
        if len(self.movement_history) < 1:
            return
        last_move = self.movement_history.pop()
        opposite_move = Movement(face=last_move.face,
                                 is_prime=not last_move.is_prime)
        self.rotate_face(opposite_move, should_store_in_history=False)

    def call_movement_callback(self):
        if self.movement_callback:
            self.movement_callback()

    def set_movement_callback(self, movement_callback):
        self.movement_callback = movement_callback 
