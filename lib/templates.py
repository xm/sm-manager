INFO_HEAD_TEMPLATE = '''\
{{
	"filesize_HH":	{fs_hh},
	"filesize_HL":	{fs_hl},
	"filesize_LH":	{fs_lh},
	"filesize_LL":	{fs_ll},
	"total_infok":	{count},
	"version":	"{version}",
	"machine_id":	"{machine}"
}}'''

SONG_META_TEMPLATE = '''\
{{
	"TL":	"{title}",
	"AT":	"{artist}",
	"GE":	"{genre}",
	"YR":	"2020",
	"PL":	0,
	"FV":	0
}}'''

NEW_INFO_HEAD_FILE = '''\
{
	"filesize_HH":	0,
	"filesize_HL":	18036305,
	"filesize_LH":	31830512,
	"filesize_LL":	69480421,
	"total_infok":	0,
	"version":	"1705240958",
	"machine_id":	"ISM1060"
}'''

NEW_PLAYLISTS_FILE = '''\
{
	"AL":	[]
}'''

NEW_FAVORITES_FILE = '''\
{
	"AF":	[]
}'''
