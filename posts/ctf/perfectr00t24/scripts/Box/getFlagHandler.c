// main.getFlagHandler
// local variable allocation has failed, the output may be wrong!
void __golang main_getFlagHandler(github_com_gin_gonic_gin_Context *c)
{
  void *v1; // rbx
  __int128 v2; // xmm15
  net_http_Request *Request; // rcx
  runtime_hmap_0 **v4; // rax
  uintptr tab; // rcx
  void *data; // rdx
  internal_abi_Type *Type; // rbx
  __int64 Hash; // r9
  void *v9; // rax
  __int64 (__golang *v10)(void *, net_http_Request *, RTYPE *, runtime_hmap_0 **); // rsi OVERLAPPED
  const uint8 *v11; // rcx
  __int64 v12; // rdi OVERLAPPED
  __int64 v13; // rax
  _slice_uint8_0 v15; // r8
  char v16; // al
  __int64 v17; // r10
  uintptr v18; // r9
  uintptr Typ; // r11
  uintptr v20; // rax
  error_0 v21; // [rsp-20h] [rbp-60h]
  error_0 v22; // [rsp-10h] [rbp-50h]
  void *v23; // [rsp+0h] [rbp-40h]
  const char *v; // [rsp+8h] [rbp-38h] BYREF
  __int64 v_8; // [rsp+10h] [rbp-30h]
  __int64 v26; // [rsp+18h] [rbp-28h]
  __int128 v27; // [rsp+20h] [rbp-20h]
  runtime_hmap_0 **v28; // [rsp+30h] [rbp-10h]
  string_0 v30; // 0:rax.8,8:rbx.8
  github_com_gin_gonic_gin_render_Render v31; // 0:rcx.8,8:rdi.8
  github_com_gin_gonic_gin_render_Render v32; // 0:rcx.8,8:rdi.8

  Request = c->Request;
  if ( Request->Method.len != 4 || *(_DWORD *)Request->Method.str != 1414745936 )
    goto LABEL_5;
  runtime_newobject((internal_abi_Type *)&RTYPE_map_string_string, v1);
  v28 = v4;
  tab = (uintptr)github_com_gin_gonic_gin_binding_JSON.tab;
  data = github_com_gin_gonic_gin_binding_JSON.data;
  if ( github_com_gin_gonic_gin_binding_JSON.tab )
  {
    Type = github_com_gin_gonic_gin_binding_JSON.tab->Type;
    Hash = github_com_gin_gonic_gin_binding_JSON.tab->Hash;
    while ( 1 )
    {
      v17 = Hash;
      v18 = main__typeAssert_0.Cache->Mask & Hash;
      Typ = main__typeAssert_0.Cache->Entries[v18].Typ;
      if ( (internal_abi_Type *)Typ == Type )
        break;
      Hash = v17 + 1;
      if ( !Typ )
      {
        v23 = github_com_gin_gonic_gin_binding_JSON.data;
        runtime_typeAssert(&main__typeAssert_0, Type, github_com_gin_gonic_gin_binding_JSON.tab);
        data = v23;
        tab = v20;
        v4 = v28;
        goto LABEL_6;
      }
    }
    tab = main__typeAssert_0.Cache->Entries[v18].Itab;
  }
LABEL_6:
  v10 = *(__int64 (__golang **)(void *, net_http_Request *, RTYPE *, runtime_hmap_0 **))(tab + 24);
  if ( !v10(data, c->Request, &RTYPE__ptr_map_string_string, v4)
    && (v11 = &byte_888503,
        v12 = 10LL,
        runtime_mapaccess1_faststr((internal_abi_MapType *)&RTYPE_map_string_string, *v28, *(string_0 *)(&v12 - 1), v10),
        *(_QWORD *)(v13 + 8) == 25LL)
    && (runtime_memequal(), v16) )
  {
    v30.str = (uint8 *)&byte_886CF4;
    v30.len = 8LL;
    os_ReadFile(v30, *(_slice_uint8_0 *)(&v10 - 2), v15, v21, v22);
    v26 = *((_QWORD *)&v2 + 1);
    v27 = v2;
    v = "Your Flag Was Denied!";
    v_8 = 21LL;
    runtime_convT((internal_abi_Type *)&RTYPE_render_String, &v, "Your Flag Was Denied!");
    v32.tab = (internal_abi_ITab *)&go_itab_github_com_gin_gonic_gin_render_String_comma_github_com_gin_gonic_gin_render_Render;
    v32.data = v30.str;
    github_com_gin_gonic_gin__ptr_Context_Render(c, 500LL, v32);
  }
  else
  {
LABEL_5:
    v26 = *((_QWORD *)&v2 + 1);
    v27 = v2;
    v = "r00t{LITERALLY_FAKE_FLAG}";
    v_8 = 25LL;
    runtime_convT((internal_abi_Type *)&RTYPE_render_String, &v, "r00t{LITERALLY_FAKE_FLAG}");
    v31.tab = (internal_abi_ITab *)&go_itab_github_com_gin_gonic_gin_render_String_comma_github_com_gin_gonic_gin_render_Render;
    v31.data = v9;
    github_com_gin_gonic_gin__ptr_Context_Render(c, 200LL, v31);
  }
}
