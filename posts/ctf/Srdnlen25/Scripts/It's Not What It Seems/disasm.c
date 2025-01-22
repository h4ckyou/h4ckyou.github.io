int __fastcall main(int argc, const char **argv, const char **envp)
{
  int result; // eax
  char *v4; // rdi
  _BYTE *i; // rsi
  _QWORD v6[3]; // [rsp+410h] [rbp-470h] BYREF
  _QWORD v7[3]; // [rsp+428h] [rbp-458h]
  char s[1024]; // [rsp+440h] [rbp-440h] BYREF
  _BYTE v9[16]; // [rsp+840h] [rbp-40h] BYREF
  _BYTE v10[32]; // [rsp+850h] [rbp-30h] BYREF

  if ( sub_401090(v10, 0x20LL) )
  {
    if ( sub_401090(v9, 16LL) )
    {
      puts("FLAG: ");
      fgets(s, 1024, stdin);
      v4 = s;
      s[strcspn(s, "\n")] = 0;
      v6[0] = 0x3B2E252C2E243233LL;
      v6[1] = 0x32341F327336732ELL;
      v6[2] = 0x1F7328141F347535LL;
      v7[0] = 0x2E35261F2E71742DLL;
      result = 0x34232E35;
      *(v7 + 6) = 0x3D2E707134232E35LL;
      for ( i = v6; ; ++i )
      {
        LOBYTE(result) = *i;
        if ( (*i ^ *v4) != 0x40 )
          break;
        ++v4;
        if ( result == 61 )
          return result;
      }
      sub_4010A0("Nope!");
      return 0;
    }
    else
    {
      sub_4010D0("Error generating random IV.\n", 1LL, 28LL, stderr);
      return 1;
    }
  }
  else
  {
    sub_4010D0("Error generating random key.\n", 1LL, 29LL, stderr);
    return 1;
  }
}