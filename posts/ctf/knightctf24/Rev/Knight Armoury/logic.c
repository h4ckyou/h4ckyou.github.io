char *a = "IaMaKnight"

__int64 __fastcall sub_401835(char *a1)
{
  __int64 result; // rax
  char v2; // [rsp+13h] [rbp-5h]
  int i; // [rsp+14h] [rbp-4h]

  for ( i = 0; ; ++i )
  {
    result = (unsigned __int8)a1[i];
    if ( !(_BYTE)result )
      break;
    v2 = a1[i];
    if ( v2 <= 96 || v2 > 122 )
    {
      if ( v2 > 64 && v2 <= 90 )
        v2 = (v2 - 52) % 26 + 65;
    }
    else
    {
      v2 = (v2 - 84) % 26 + 97;
    }
    a1[i] = v2;
  }
  return result;
}

__int64 __fastcall sub_401905(char *a1, int a2)
{
  __int64 result; // rax
  int i; // [rsp+18h] [rbp-4h]

  for ( i = 0; ; ++i )
  {
    result = (unsigned __int8)a1[i];
    if ( !(_BYTE)result )
      break;
    if ( a1[i] <= 96 || a1[i] > 122 )
    {
      if ( a1[i] > 64 && a1[i] <= 90 )
        a1[i] = (a1[i] - 65 + a2) % 26 + 65;
    }
    else
    {
      a1[i] = (a1[i] - 97 + a2) % 26 + 97;
    }
  }
  return result;
}

r = "YqCqAdywxj"
