HOST = "139.198.19.224" 
PORT = 1883
USER = "pabox"
PASS = "1qaz2wsx3edc"
QoS  = 1
HTTP = 9000
SUB_TOPIC = "PABOX"
MY_HOST = "127.0.0.1"
MY_USER = "iot"
MY_PASS = "iot"
MY_DATABASE ="pabox"

# SUBSCRIBE codes those need to Publish back
MUST_REPLY_CODES = ('01','02',)

## mysql
GET_SQL={
    "add_trandata":("INSERT INTO `pabox`.`trandata`(`imei`,`code`,`code_name`,`seq`,`attr01`,`desc`,`data`) VALUES (%s, %s, %s, %s, %s, %s, %s)"),
    "trandata":("SELECT * from `pabox`.`trandata` order by `line_id` desc limit 100"),
    "item":("SELECT * from `pabox`.`item`"),
    "code_detail":("SELECT * from `pabox`.`code_detail`"),
    }


