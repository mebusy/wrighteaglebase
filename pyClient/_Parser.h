enum ObjectType
{
	OBJ_Line,
	OBJ_Ball,
	OBJ_Marker,
	OBJ_Marker_Behind,  /* Not seen */
	OBJ_Player,
	OBJ_None
};

enum SideLineType
{
	SL_Left = 0,
	SL_Right,
	SL_Top,
	SL_Bottom,

	SL_MAX,
	SL_NONE
};

enum MarkerType
{
	Goal_L = 0,
	Goal_R,

	Flag_C,
	Flag_CT,
	Flag_CB,
	Flag_LT,
	Flag_LB,
	Flag_RT,
	Flag_RB,

	Flag_PLT,
	Flag_PLC,
	Flag_PLB,
	Flag_PRT,
	Flag_PRC,
	Flag_PRB,

	Flag_GLT,
	Flag_GLB,
	Flag_GRT,
	Flag_GRB,

	Flag_TL50,
	Flag_TL40,
	Flag_TL30,
	Flag_TL20,
	Flag_TL10,
	Flag_T0,
	Flag_TR10,
	Flag_TR20,
	Flag_TR30,
	Flag_TR40,
	Flag_TR50,

	Flag_BL50,
	Flag_BL40,
	Flag_BL30,
	Flag_BL20,
	Flag_BL10,
	Flag_B0,
	Flag_BR10,
	Flag_BR20,
	Flag_BR30,
	Flag_BR40,
	Flag_BR50,

	Flag_LT30,
	Flag_LT20,
	Flag_LT10,
	Flag_L0,
	Flag_LB10,
	Flag_LB20,
	Flag_LB30,

	Flag_RT30,
	Flag_RT20,
	Flag_RT10,
	Flag_R0,
	Flag_RB10,
	Flag_RB20,
	Flag_RB30,

	FLAG_MAX,
	FLAG_NONE
};


