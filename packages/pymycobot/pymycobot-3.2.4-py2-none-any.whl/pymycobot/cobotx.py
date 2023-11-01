# coding=utf-8

import time
import math
import numpy as np

from pymycobot.generate import CommandGenerator
from pymycobot.common import ProtocolCode, write, read
from pymycobot.error import calibration_parameters

coff = 180 / math.pi
inv_coff = math.pi / 180

def cvt_euler_angle_to_rotation_matrix(ptr_euler_angle):
    ptr_sin_angle = np.sin(ptr_euler_angle)
    ptr_cos_angle = np.cos(ptr_euler_angle)

    ptr_rotation_matrix = np.zeros((3, 3))
    ptr_rotation_matrix[0, 0] = ptr_cos_angle[2] * ptr_cos_angle[1]
    ptr_rotation_matrix[0, 1] = ptr_cos_angle[2] * ptr_sin_angle[1] * ptr_sin_angle[0] - ptr_sin_angle[2] * ptr_cos_angle[0]
    ptr_rotation_matrix[0, 2] = ptr_cos_angle[2] * ptr_sin_angle[2] * ptr_cos_angle[0] + ptr_sin_angle[2] * ptr_sin_angle[0]
    ptr_rotation_matrix[1, 0] = ptr_sin_angle[2] * ptr_cos_angle[1]
    ptr_rotation_matrix[1, 1] = ptr_sin_angle[2] * ptr_sin_angle[1] * ptr_sin_angle[0] + ptr_cos_angle[2] * ptr_cos_angle[0]
    ptr_rotation_matrix[1, 2] = ptr_sin_angle[2] * ptr_sin_angle[1] * ptr_cos_angle[0] - ptr_cos_angle[2] * ptr_sin_angle[0]
    ptr_rotation_matrix[2, 0] = -ptr_sin_angle[1]
    ptr_rotation_matrix[2, 1] = ptr_cos_angle[1] * ptr_sin_angle[0]
    ptr_rotation_matrix[2, 2] = ptr_cos_angle[1] * ptr_cos_angle[0]
    
    return ptr_rotation_matrix

def cvt_rotation_matrix_to_euler_angle(rotation_matrix):
    euler_angle = np.zeros(3)
    euler_angle[2] = np.arctan2(rotation_matrix[1, 0], rotation_matrix[0, 0])

    f_cos_roll = np.cos(euler_angle[2])
    f_sin_roll = np.sin(euler_angle[2])

    euler_angle[1] = np.arctan2(-rotation_matrix[2, 0], (f_cos_roll * rotation_matrix[0, 0]) + (f_sin_roll * rotation_matrix[1, 0]))
    euler_angle[0] = np.arctan2((f_sin_roll * rotation_matrix[0, 2]) - (f_cos_roll * rotation_matrix[1, 2]), (-f_sin_roll * rotation_matrix[0, 1]) + (f_cos_roll * rotation_matrix[1, 1]))

    return euler_angle

def base_to_single(posture, dire):
    position = np.array(posture[:3])
    rotation = np.array(posture[3:])
    matrix = cvt_euler_angle_to_rotation_matrix(rotation)
    T = np.vstack((np.hstack((matrix, position.reshape(3, 1))), np.array([0, 0, 0, 1])))
    # L1 = 38.42  # 131.42 - 93
    L2 = 310
    # eccentricity = 31.97
    af = np.pi / 6
    TRB = np.array([[np.cos(af), np.sin(af), 0,  27.6868],
                    [0, 0, 1, -L2],
                    [np.sin(af), -np.cos(af), 0, -22.435],
                    [0, 0, 0, 1]])
    TLB = np.array([[np.cos(af), -np.sin(af), 0,  27.6868],
                    [0, 0, -1, L2],
                    [np.sin(af), np.cos(af), 0, -22.435],
                    [0, 0, 0, 1]])

    if dire == 0:
        Tp = np.dot(TLB, T)
    else:
        Tp = np.dot(TRB, T)

    rotation_matrix = Tp[:3, :3]
    position = Tp[:3, 3]
    rotation = cvt_rotation_matrix_to_euler_angle(rotation_matrix)

    return np.hstack((position, rotation))

def single_to_base(posture, dire):
    posture = np.array(posture)
    rotation = posture[3:]
    matrix = cvt_euler_angle_to_rotation_matrix(rotation)
    T = np.vstack((np.hstack((matrix, posture[:3].reshape(3, 1))), np.array([0, 0, 0, 1])))
    L1 = 38.42  # 131.42 - 93
    L2 = 310
    eccentricity = 31.97
    af = np.pi / 6
    TBR = np.array([[np.cos(af), 0, np.sin(af), L1 * np.sin(af) - eccentricity],
                    [np.sin(af), 0, -np.cos(af), -L1 * np.cos(af)],
                    [0, 1, 0, L2],
                    [0, 0, 0, 1]])
    TBL = np.array([[np.cos(af), 0, np.sin(af), L1 * np.sin(af) - eccentricity],
                    [-np.sin(af), 0, np.cos(af), L1 * np.cos(af)],
                    [0, -1, 0, L2],
                    [0, 0, 0, 1]])
    if dire == 1:
        TBF = np.dot(TBR, T)
    else:
        TBF = np.dot(TBL, T)

    rotation_matrix = TBF[:3, :3]
    position = TBF[:3, 3]
    rotation = cvt_rotation_matrix_to_euler_angle(rotation_matrix)

    return np.hstack((position, rotation))

class CobotX(CommandGenerator):
    _write = write
    _read = read
    def __init__(self, port, baudrate="115200", timeout=0.1, debug=False):
        """
        Args:
            port     : port string
            baudrate : baud rate string, default '115200'
            timeout  : default 0.1
            debug    : whether show debug info
        """
        super(CobotX, self).__init__(debug)
        self.calibration_parameters = calibration_parameters
        import serial

        self._serial_port = serial.Serial()
        self._serial_port.port = port
        self._serial_port.baudrate = baudrate
        self._serial_port.timeout = timeout
        self._serial_port.rts = False
        self._serial_port.open()
        

    def _mesg(self, genre, *args, **kwargs):
        """

        Args:
            genre: command type (Command)
            *args: other data.
                   It is converted to octal by default.
                   If the data needs to be encapsulated into hexadecimal,
                   the array is used to include them. (Data cannot be nested)
            **kwargs: support `has_reply`
                has_reply: Whether there is a return value to accept.
        """
        real_command, has_reply = super(CobotX, self)._mesg(genre, *args, **kwargs)
        self._write(self._flatten(real_command))

        if has_reply:
            data = self._read(genre)
            if genre == ProtocolCode.SET_SSID_PWD:
                return None
            res = self._process_received(data, genre)
            if genre in [
                ProtocolCode.ROBOT_VERSION,
                ProtocolCode.GET_ROBOT_ID,
                ProtocolCode.IS_POWER_ON,
                ProtocolCode.IS_CONTROLLER_CONNECTED,
                ProtocolCode.IS_PAUSED,  # TODO have bug: return b''
                ProtocolCode.IS_IN_POSITION,
                ProtocolCode.IS_MOVING,
                ProtocolCode.IS_SERVO_ENABLE,
                ProtocolCode.IS_ALL_SERVO_ENABLE,
                ProtocolCode.GET_SERVO_DATA,
                ProtocolCode.GET_DIGITAL_INPUT,
                ProtocolCode.GET_GRIPPER_VALUE,
                ProtocolCode.IS_GRIPPER_MOVING,
                ProtocolCode.GET_SPEED,
                ProtocolCode.GET_ENCODER,
                ProtocolCode.GET_BASIC_INPUT,
                ProtocolCode.GET_TOF_DISTANCE,
                ProtocolCode.GET_END_TYPE,
                ProtocolCode.GET_MOVEMENT_TYPE,
                ProtocolCode.GET_REFERENCE_FRAME,
                ProtocolCode.GET_FRESH_MODE,
                ProtocolCode.GET_GRIPPER_MODE,
                ProtocolCode.SET_SSID_PWD,
                ProtocolCode.COBOTX_IS_GO_ZERO,
                ProtocolCode.GET_ERROR_DETECT_MODE
            ]:
                return self._process_single(res)
            elif genre in [ProtocolCode.GET_ANGLES]:
                return [self._int2angle(angle) for angle in res]
            elif genre in [
                ProtocolCode.GET_COORDS,
                ProtocolCode.GET_TOOL_REFERENCE,
                ProtocolCode.GET_WORLD_REFERENCE,
            ]:
                if res:
                    r = []
                    for idx in range(3):
                        r.append(self._int2coord(res[idx]))
                    for idx in range(3, 6):
                        r.append(self._int2angle(res[idx]))
                    return r
                else:
                    return res
            elif genre in [ProtocolCode.GET_SERVO_VOLTAGES]:
                return [self._int2coord(angle) for angle in res]
            elif genre in [ProtocolCode.GET_BASIC_VERSION, ProtocolCode.SOFTWARE_VERSION, ProtocolCode.GET_ATOM_VERSION]:
                return self._int2coord(self._process_single(res))
            elif genre in [
                ProtocolCode.GET_JOINT_MAX_ANGLE,
                ProtocolCode.GET_JOINT_MIN_ANGLE,
            ]:
                return self._int2coord(res[0])
            elif genre == ProtocolCode.GET_ANGLES_COORDS:
                r = []
                for index in range(len(res)):
                    if index < 7:
                        r.append(self._int2angle(res[index]))
                    elif index < 10:
                        r.append(self._int2coord(res[index]))
                    else:
                        r.append(self._int2angle(res[index]))
                return r
            elif genre == ProtocolCode.GO_ZERO:
                r = []
                if res:
                    if 1 not in res[1:]:
                        return res[0]
                    else:
                        for i in range(1, len(res)):
                            if res[i] == 1:
                                r.append(i)
                return r
            elif genre in [ProtocolCode.COBOTX_GET_ANGLE, ProtocolCode.COBOTX_GET_SOLUTION_ANGLES]:
                    return self._int2angle(res[0])
            else:
                return res
        return None

    def set_solution_angles(self, angle, speed):
        """Set zero space deflection angle value

        Args:
            angle: Angle of joint 1. The angle range is -90 ~ 90
            speed: 1 - 100.
        """
        self.calibration_parameters(
            class_name=self.__class__.__name__, speed=speed, solution_angle=angle
        )
        return self._mesg(
            ProtocolCode.COBOTX_SET_SOLUTION_ANGLES, [self._angle2int(angle)], speed
        )

    def get_solution_angles(self):
        """Get zero space deflection angle value"""
        return self._mesg(ProtocolCode.COBOTX_GET_SOLUTION_ANGLES, has_reply=True)

    def write_move_c(self, transpoint, endpoint, speed):
        """_summary_

        Args:
            transpoint (list): Arc passing point coordinates
            endpoint (list): Arc end point coordinates
            speed (int): 1 ~ 100
        """
        start = []
        end = []
        for index in range(6):
            if index < 3:
                start.append(self._coord2int(transpoint[index]))
                end.append(self._coord2int(endpoint[index]))
            else:
                start.append(self._angle2int(transpoint[index]))
                end.append(self._angle2int(endpoint[index]))
        return self._mesg(ProtocolCode.WRITE_MOVE_C, start, end, speed)

    def focus_all_servos(self):
        """Lock all joints"""
        return self._mesg(ProtocolCode.FOCUS_ALL_SERVOS)

    def go_zero(self):
        """Control the machine to return to the zero position.
        
        Return:
            1 : All motors return to zero position.
            list : Motor with corresponding ID failed to return to zero.
        """
        return self._mesg(ProtocolCode.GO_ZERO, has_reply=True)

    def get_angle(self, joint_id):
        """Get single joint angle

        Args:
            joint_id (int): 1 ~ 7 or 11 ~ 13.
        """
        self.calibration_parameters(class_name=self.__class__.__name__, id=joint_id)
        return self._mesg(ProtocolCode.COBOTX_GET_ANGLE, joint_id, has_reply=True)

    def is_gone_zero(self):
        """Check if it has returned to zero

        Return:
            1 : Return to zero successfully.
            0 : Returning to zero.
        """
        return self._mesg(ProtocolCode.COBOTX_IS_GO_ZERO, has_reply=True)

    def set_encoder(self, joint_id, encoder):
        """Set a single joint rotation to the specified potential value.

        Args:
            joint_id (int): Joint id 1 - 7.
            encoder: The value of the set encoder.
        """
        # TODO CobotX此接口待定
        # self.calibration_parameters(
        #     class_name=self.__class__.__name__, id=joint_id, encoder=encoder
        # )
        return self._mesg(ProtocolCode.SET_ENCODER, joint_id, [encoder])
    
    def servo_restore(self, joint_id):
        """Abnormal recovery of joints

        Args:
            joint_id (int): Joint ID.
                arm : 1 ~ 7 
                waist : 13
                All joints: 254
        """
        self.calibration_parameters(
            class_name=self.__class__.__name__, servo_restore=joint_id
        )
        self._mesg(ProtocolCode.SERVO_RESTORE, joint_id)
        
    def set_error_detect_mode(self, mode):
        """Set error detection mode. Turn off without saving, default to open state
        
        Return:
            mode : 0 - close 1 - open.
        """
        self.calibration_parameters(
            class_name=self.__class__.__name__, mode=mode
        )
        self._mesg(ProtocolCode.SET_ERROR_DETECT_MODE, mode)
        
    def get_error_detect_mode(self):
        """Set error detection mode"""
        return self._mesg(ProtocolCode.GET_ERROR_DETECT_MODE, has_reply=True)
    
    def sync_send_angles(self, degrees, speed, timeout=15):
        """Send the angle in synchronous state and return when the target point is reached
            
        Args:
            degrees: a list of degree values(List[float]), length 6.
            speed: (int) 0 ~ 100
            timeout: default 7s.
        """
        t = time.time()
        self.send_angles(degrees, speed)
        while time.time() - t < timeout:
            f = self.is_in_position(degrees, 0)
            if f == 1:
                break
            time.sleep(0.1)
        return self

    def sync_send_coords(self, coords, speed, mode=None, timeout=15):
        """Send the coord in synchronous state and return when the target point is reached
            
        Args:
            coords: a list of coord values(List[float])
            speed: (int) 0 ~ 100
            mode: (int): 0 - angular（default）, 1 - linear
            timeout: default 7s.
        """
        t = time.time()
        self.send_coords(coords, speed, mode)
        while time.time() - t < timeout:
            if self.is_in_position(coords, 1) == 1:
                break
            time.sleep(0.1)
        return self
    
    def dual_get_base_coords(self):
        """get Base coords.

        Returns:
            list: Base_posture
        """
        coords = self.get_coords()
        for i in range(3):
            coords[3+i] *= inv_coff
        if self._serial_port.baudrate == "dev/ttyS0":
            Base_posture = single_to_base(coords, 1)
        elif self._serial_port.baudrate == "dev/ttyTHS1":
            Base_posture = single_to_base(coords, 0)
        Base_posture[3:] *= coff
        
        return list(Base_posture)
    
    def dual_write_base_coords(self, Base_posture, speed):
        """write base coords

        Args:
            Base_posture (list): Base_posture data
            speed (int): speed range 1 - 100.
        """
        self.calibration_parameters(
            class_name=self.__class__.__name__, speed=speed
        )
        base = np.array(Base_posture)
        base[3:] *= inv_coff
        if self._serial_port.baudrate == "dev/ttyS0":
            Single_posture = base_to_single(base, 1)
        elif self._serial_port.baudrate == "dev/ttyTHS1":
            Single_posture = base_to_single(base, 0)
        
        Single_posture[3:] *= coff
        self.send_coords(Single_posture, speed, 1)
        