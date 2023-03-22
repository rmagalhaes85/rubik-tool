import random
from collections import namedtuple

FACES = ['front', 'back', 'up', 'down', 'left', 'right']
AXES = ['x', 'y', 'z']

Cubelets = namedtuple('Cubelets', FACES)

CubeMovement = namedtuple('CubeMovement', ['axis'])
CubeMovement.__repr__ = lambda self: f'{self.axis} (axis)'

FaceMovement = namedtuple('FaceMovement', ['face', 'is_prime'])
FaceMovement.__repr__ = lambda self: f'{self.face}{chr(39) if self.is_prime else ""}'

def debug_init():
    global pp
    global c
    from pprint import pprint
    pp = pprint
    c = Cube()
    c.shuffle()
    #c.rotate_face('F')
    #c.rotate_cube('x')
    #c.rotate_face('B')

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
            down=''.join((d2, d3, d4, d5, d6, d7, d0, d1, d8)),
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
        self.movement_callbacks = []
        self.movement_history = []
        self.movement_history_pointer = -1
        self.reset(should_callback=False)
        self.filename = None

    def initialize_cubelets(self):
        self.cubelets = create_default_cubelets()

    def set_cubelets(self, cubelets, should_callback=True):
        self.cubelets = cubelets
        if should_callback:
            self.call_movement_callbacks()

    def reset(self, should_callback=True):
        self.initialize_cubelets()
        self.movement_history.clear()
        self.movement_history_pointer = -1
        if should_callback:
            self.call_movement_callbacks()

    def rotate_face(self, movement_str, should_store_in_history=True):
        face_movement = parse_face_movement(movement_str)
        if should_store_in_history:
            self._append_movement(face_movement)
        self._apply_movement(face_movement)

    def rotate_cube(self, axis, is_ccw=False, should_store_in_history=True):
        cube_movement = parse_cube_movement(axis)
        if should_store_in_history:
            self._append_movement(cube_movement)
        self._apply_movement(cube_movement)

    def shuffle(self):
        n_moves = 20
        faces = random.choices([f[0] for f in FACES], k=n_moves)
        primes = random.choices(["", "'"], k=n_moves)
        for move_elements in zip(faces, primes):
            self.rotate_face(''.join(move_elements))

    def set_movement_history_pointer(self, pointer):
        if not -1 <= pointer < len(self.movement_history):
            raise ValueError(
                "pointer must be -1 or lie within movement_history's valid range"
            )
        if pointer == self.movement_history_pointer:
            return
        direction = 1 if (pointer - self.movement_history_pointer) > 0 else -1
        while pointer != self.movement_history_pointer:
            if direction > 0:
                next_movement = self.movement_history[self.movement_history_pointer + 1]
                self._apply_movement(next_movement, should_callback=False)
            else:
                current_movement = self.movement_history[self.movement_history_pointer]
                self._unapply_movement(current_movement, should_callback=False)
            self.movement_history_pointer += direction
        self.call_movement_callbacks()

    def call_movement_callbacks(self):
        [c() for c in self.movement_callbacks]

    def add_movement_callback(self, movement_callback):
        self.movement_callbacks.append(movement_callback)

    def remove_movement_callback(self, movement_callback):
        self.movement_callbacks.remove(movement_callback)

    def _append_movement(self, movement):
        self.movement_history = self.movement_history[0:self.movement_history_pointer + 1]
        self.movement_history.append(movement)
        self.movement_history_pointer += 1

    def _remove_current_movement(self):
        if self.movement_history_pointer < 0:
            return
        self.movement_history = self.movement_history[0:self.movement_history_pointer + 1]
        self.movement_history_pointer -= 1

    def _apply_movement(self, movement, should_callback=True):
        if isinstance(movement, FaceMovement):
            self._rotate_face(movement, should_callback)
        elif isinstance(movement, CubeMovement):
            self._rotate_cube(movement, should_callback)
        else:
            raise ValueError(f'Unknown movement type: {type(movement)}')

    def _unapply_movement(self, movement, should_callback=True):
        if isinstance(movement, FaceMovement):
            inverted_movement = FaceMovement(face=movement.face,
                                             is_prime=not movement.is_prime)
            self._apply_movement(inverted_movement, should_callback)
        elif isinstance(movement, CubeMovement):
            for _ in range(0, 3):
                self._apply_movement(movement, should_callback)
        else:
            raise ValueError(f'Unknown movement type: {type(movement)}')

    def _rotate_face(self, face_movement, should_callback=True):
        rotated_cubelets = apply_face_rotation(self.cubelets, face_movement)
        self.cubelets = rotated_cubelets
        if should_callback:
            self.call_movement_callbacks()

    def _rotate_cube(self, cube_movement, should_callback=True):
        rotated_cubelets = apply_cube_rotation(self.cubelets, cube_movement)
        self.cubelets = rotated_cubelets
        if should_callback:
            self.call_movement_callbacks()

if __name__ == '__main__':
    debug_init()
