message_type_ack = {
    
    0x00 : {
        "description" : "TCP Heartbeat",
        "Send" : [],
        "ACK" : []
    },

    0x01 : {
        "description" : "Request Gimbal Camera Firmware Version",
        "Send" : [],
        "ACK" : [
            {
            "name" : "code_board_ver",
            "type" : "raw"
            }, 
            {
            "name" : "gimbal_firmware_ver",
            "type" : "raw"
            },
            {
            "name" : "zoom_firmware_ver",
            "type" : "raw"
            }
        ]
    },
    # Request Gimbal Camera Hardware ID
    0x02 : {
        "description" : "Request Gimbal Camera Hardware ID",
        "Send" : [],
        "ACK" : [{
            "name" : "hardware_id",
            0x6B: "ZR10",
            0x73: "A8 mini",
            0x75: "A2 mini",
            0x78: "ZR30",
            0x82: "ZT6",
            0x7A: "ZT30",
        }]
    },

    0x03 : {

    },

    0x04 : {
        "description" : "Auto Focus",
        "Send" : [
            {
                "name" : "auto_focus",
                1 : "start auto focus for once"
            },
            {
                "name" : "touch_x"
            },
            {
                "name" : "touch_y"
            }
        ],
        "ACK" : [{
            "name" : "sta",
            1 : "success",
            0 : "failure"
        }]
    },

    0x05 : {
        "description" : "Manual Zoom and Auto Focus",
        "Send" : [
            {
                "name" : "zoom",
                1 : "start zoom in",
                0 : "stop zoom in/out",
                -1 : "start zoom out"
            }
        ],
        "ACK" : [
            {
            "name" : "multiple zoom"
        }]
    },

    0x06 : {

    },

    0x07 : {

    },

    0x08 : {

    },

    0x09 : {

    },

    0x0A : {

    },
    
    0x0B : {

    },

    0x0C : {

    },

    0x0D : {

    },

    0x0E : {

    },

    0x0F : {
        "description" : "absolute zoom and auto focus",
        "Send" : [
            {
                "name" : "absolute_movement",
                "min" : 0x10,
                "max" : 0x1E
            },
            {
                "name" : "absolute_movement_float",
                "min" : 0x0,
                "max" : 0x9
            }
        ],
        "ACK" : []

    },

    0x10 : {

    },

    0x11 : {

    },

    0x12 : {

    },

    0x13 : {

    },

    0x14 : {

    },

    0x15 : {

    },

    0x16 : {

    },

    0x17 : {

    },
    
    0x18 : {

    },

    0x19 : {
        "description" : "Request Gimbal Camera's Present Working Mode",
        "Send" : [],
        "ACK" : [{
            "name" : "gimbal_mode",
            0x00 : "Lock Mode",
            0x01 : "Follow Mode",
            0x02 : "FPV Mode"
        }]

    },

    0x1A : {

    },

    0x1B : {

    },

    0x1C : {

    },

    0x1D : {

    },

    0x1E : {

    },

    0x1F : {

    },


}