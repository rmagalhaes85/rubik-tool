from collections import namedtuple

FACES = ['front', 'back', 'up', 'down', 'left', 'right']
AXES = ['x', 'y', 'z']

Cubelets = namedtuple('Cubelets', FACES)

CubeMovement = namedtuple('CubeMovement', ['axis'])

FaceMovement = namedtuple('FaceMovement', ['face', 'is_prime'])

def parse_face_movement(movement):
    assert len(movement) == 1 or (len(movement) == 2 and movement[1] == "'")
    face = movement[0].lower()
    assert face in [f[0] for f in FACES]
    is_prime = len(movement) == 2 and movement[1] == "'"
    return FaceMovement(face=face, is_prime=is_prime)

def parse_cube_movement(movement):
    assert movement in AXES
    return CubeMovement(axis=movement)

def apply_face_rotation(cubelets, face_movement):
    c = (
        apply_face_rotation(
            apply_face_rotation(cubelets,
                                FaceMovement(face=face_movement.face,
                                             is_prime=not face_movement.is_prime)),
            FaceMovement(face=face_movement.face,
                         is_prime=not face_movement.is_prime)
        )
    ) if face_movement.is_prime else cubelets
    face = face_movement.face
    (f0, f1, f2, f3, f4, f5, f6, f7, f8) = getattr(c, 'front')
    (b0, b1, b2, b3, b4, b5, b6, b7, b8) = getattr(c, 'back')
    (u0, u1, u2, u3, u4, u5, u6, u7, u8) = getattr(c, 'up')
    (d0, d1, d2, d3, d4, d5, d6, d7, d8) = getattr(c, 'down')
    (l0, l1, l2, l3, l4, l5, l6, l7, l8) = getattr(c, 'left')
    (r0, r1, r2, r3, r4, r5, r6, r7, r8) = getattr(c, 'right')
    if face == 'f':
        return Cubelets(
            front=''.join((f6, f7, f0, f1, f2, f3, f4, f5, f8)),
            back=c.back,
            up=''.join((u0, u1, u2, l1, l2, l3, u6, u7, u8)),
            down=''.join((r6, r7, d2, d3, d4, d5, d6, r5, d8)),
            left=''.join((l0, d7, d0, d1, l4, l5, l6, l7, l8)),
            right=''.join((r0, r1, r2, r3, r4, u3, u4, u5, r8)),
        )
    elif face == 'b':
        return Cubelets(
            front=c.front,
            back=''.join((b6, b7, b0, b1, b2, b3, b4, b5, b8)),
            up=''.join((r2, r3, u2, u3, u4, u5, u6, r1, u8)),
            down=''.join((d0, d1, d2, l5, l6, l7, d6, d7, d8)),
            left=''.join((l0, l1, l2, l3, l4, u7, u0, u1, l8)),
            right=''.join((r0, d3, d4, d5, r4, r5, r6, r7, r8)),
        )
    elif face == 'u':
        return Cubelets(
            front=''.join((r0, r1, f2, f3, f4, f5, f6, r7, f8)),
            back=''.join((l0, l1, b2, b3, b4, b5, b6, l7, b8)),
            up=''.join((u6, u7, u0, u1, u2, u3, u4, u5, u8)),
            down=c.down,
            left=''.join((f0, f1, l2, l3, l4, l5, l6, f7, l8)),
            right=''.join((b0, b1, r2, r3, r4, r5, r6, b7, r8)),
        )
    elif face == 'd':
        return Cubelets(
            front=''.join((f0, f1, f2, l3, l4, l5, f6, f7, f8)),
            back=''.join((b0, b1, b2, r3, r4, r5, b6, b7, b8)),
            up=c.up,
            down=''.join((d6, d7, d0, d1, d2, d3, d4, d5, d8)),
            left=''.join((l0, l1, l2, b3, b4, b5, l6, l7, l8)),
            right=''.join((r0, r1, r2, f3, f4, f5, r6, r7, r8)),
        )
    elif face == 'l':
        return Cubelets(
            front=''.join((f0, f1, f2, f3, f4, u5, u6, u7, f8)),
            back=''.join((b0, d5, d6, d7, b4, b5, b6, b7, b8)),
            up=''.join((u0, u1, u2, u3, u4, b1, b2, b3, u8)),
            down=''.join((d0, d1, d2, d3, d4, f5, f6, f7, d8)),
            left=''.join((l6, l7, l0, l1, l2, l3, l4, l5, l8)),
            right=c.right,
        )
    elif face == 'r':
        return Cubelets(
            front=''.join((f0, d1, d2, d3, f4, f5, f6, f7, f8)),
            back=''.join((b0, b1, b2, b3, b4, u1, u2, u3, b8)),
            up=''.join((u0, f1, f2, f3, u4, u5, u6, u7, u8)),
            down=''.join((d0, b5, b6, b7, d4, d5, d6, d7, d8)),
            left=c.left,
            right=''.join((r6, r7, r0, r1, r2, r3, r4, r5, r8)),
        )
    raise ValueError(f'Invalid movement {movement=}')

def apply_cube_rotation(cubelets, movement):
    axis = movement.axis
    assert axis in AXES
    (f0, f1, f2, f3, f4, f5, f6, f7, f8) = getattr(cubelets, 'front')
    (b0, b1, b2, b3, b4, b5, b6, b7, b8) = getattr(cubelets, 'back')
    (u0, u1, u2, u3, u4, u5, u6, u7, u8) = getattr(cubelets, 'up')
    (d0, d1, d2, d3, d4, d5, d6, d7, d8) = getattr(cubelets, 'down')
    (l0, l1, l2, l3, l4, l5, l6, l7, l8) = getattr(cubelets, 'left')
    (r0, r1, r2, r3, r4, r5, r6, r7, r8) = getattr(cubelets, 'right')
    if axis == 'x':
        return Cubelets(
            front=cubelets.down,
            back=''.join((u4, u5, u6, u7, u0, u1, u2, u3, u8)),
            up=cubelets.front,
            down=''.join((b4, b5, b6, b7, b0, b1, b2, b3, b8)),
            left=''.join((l2, l3, l4, l5, l6, l7, l0, l1, l8)),
            right=''.join((r6, r7, r0, r1, r2, r3, r4, r5, r8)),
        )
    elif axis == 'y':
        return Cubelets(
            front=''.join((f6, f7, f0, f1, f2, f3, f4, f5, f8)),
            back=''.join((b6, b7, b0, b1, b2, b3, b4, b5, b8)),
            up=''.join((l6, l7, l0, l1, l2, l3, l4, l5, l8)),
            down=''.join((r6, r7, r0, r1, r2, r3, r4, r5, r8)),
            left=''.join((d6, d7, d0, d1, d2, d3, d4, d5, d8)),
            right=''.join((u6, u7, u0, u1, u2, u3, u4, u5, u8)),
        )
    elif axis == 'z':
        return Cubelets(
            front=cubelets.right,
            back=cubelets.left,
            up=''.join((u6, u7, u0, u1, u2, u3, u4, u5, u8)),
            down=''.join((d6, d7, d0, d1, d2, d3, d4, d5, d8)),
            left=cubelets.front,
            right=cubelets.back,
        )
    return ValueError('Unknown axis {axis=}')

def create_default_cubelets():
    return Cubelets(
        front=('W' * 9),
        back=('Y' * 9),
        up=('O' * 9),
        down=('R' * 9),
        left=('G' * 9),
        right=('B' * 9),
    )

class Cube:

    def __init__(self):
        self.movement_callback = None
        self.movement_history = []
        self.reset(should_callback=False)

    def initialize_cubelets(self):
        self.cubelets = create_default_cubelets()

    def get_cubelets(self):
        return self.cubelets

    def reset(self, should_callback=True):
        self.initialize_cubelets()
        self.movement_history.clear()
        if should_callback:
            self.call_movement_callback()

    def rotate_face(self, movement, should_store_in_history=True):
        face_movement = parse_face_movement(movement)
        return self.rotate_face_(face_movement, should_store_in_history)

    def rotate_face_(self, face_movement, should_store_in_history=True):
        rotated_cubelets = apply_face_rotation(self.cubelets, face_movement)
        self.cubelets = rotated_cubelets
        if should_store_in_history:
            self.movement_history.append(face_movement)
        self.call_movement_callback()

    def rotate_cube(self, axis, is_ccw=False, should_store_in_history=True):
        cube_movement = parse_cube_movement(axis)
        return self.rotate_cube_(cube_movement, should_store_in_history)

    def rotate_cube_(self, cube_movement, should_store_in_history):
        rotated_cubelets = apply_cube_rotation(self.cubelets, cube_movement)
        self.cubelets = rotated_cubelets
        if should_store_in_history:
            self.movement_history.append(cube_movement)
        self.call_movement_callback()

    def undo_movement(self):
        if len(self.movement_history) < 1:
            return
        last_movement = self.movement_history.pop()
        assert type(last_movement) in [CubeMovement, FaceMovement]
        if isinstance(last_movement, FaceMovement):
            self.rotate_face_(FaceMovement(face=last_movement.face,
                                           is_prime=not last_movement.is_prime),
                              should_store_in_history=False)
        elif isinstance(last_movement, CubeMovement):
            self.rotate_cube_(CubeMovement(axis=last_movement.axis),
                              should_store_in_history=False)
            self.rotate_cube_(CubeMovement(axis=last_movement.axis),
                              should_store_in_history=False)
            self.rotate_cube_(CubeMovement(axis=last_movement.axis),
                              should_store_in_history=False)

    def call_movement_callback(self):
        if self.movement_callback:
            self.movement_callback()

    def set_movement_callback(self, movement_callback):
        self.movement_callback = movement_callback
