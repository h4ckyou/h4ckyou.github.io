package com.knightctf.knights_droid;

import android.content.Context;

public class SecretKeyVerifier {
    private stayVtic final String ENC_SEG_A = "wp5_GJECD";
    private static final String ENC_SEG_B = "P_u0q_c0p_";
    private static final String ENC_SEG_C = "GYPB{_ykjcn";
    private static final String ENC_SEG_D = "uKqN_Gj1cd7_zN01z_}";

    public static boolean verifyFlag(Context context, String userInput) {
        String fullPackageName = context.getPackageName();
        if (fullPackageName.length() < 20) {
            return false;
        }
        return "GYPB{_ykjcnwp5_GJECDP_u0q_c0p_uKqN_Gj1cd7_zN01z_}".equals(droidMagic(userInput, computeShiftFromKey(fullPackageName.substring(0, 10))));
    }

    private static int computeShiftFromKey(String key) {
        int sum = 0;
        for (char c : key.toCharArray()) {
            sum += c;
        }
        return sum % 26;
    }

    private static String droidMagic(String input, int droidTask) {
        int droidTask2 = ((droidTask % 26) + 26) % 26;
        StringBuilder sb = new StringBuilder();
        for (char c : input.toCharArray()) {
            if (Character.isUpperCase(c)) {
                sb.append((char) ((((c - 'A') + droidTask2) % 26) + 65));
            } else if (Character.isLowerCase(c)) {
                sb.append((char) ((((c - 'a') + droidTask2) % 26) + 97));
            } else {
                sb.append(c);
            }
        }
        return sb.toString();
    }
}
