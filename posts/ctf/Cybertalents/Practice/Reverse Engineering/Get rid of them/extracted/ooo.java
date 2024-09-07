package ctf;

import java.util.Base64;

public class ooo {
   public String _1(String a) {
      try {
         return new String(Base64.getDecoder().decode(a));
      } catch (Exception var3) {
         System.out.println("Wrong argsssss");
         System.out.println(a);
         return "";
      }
   }

   public String _2(String a, String[] b) {
      String temp = "";
      int i = 0;
      int j = false;

      for(boolean bad = false; i != a.length(); ++i) {
         int j = 0;

         for(bad = false; j != b.length; ++j) {
            if (a.charAt(i) == Integer.parseInt(b[j])) { 
               bad = true;
            }
         }

         if (!bad) {
            temp = temp + a.charAt(i);
         }
      }

      return temp;
   }
}
