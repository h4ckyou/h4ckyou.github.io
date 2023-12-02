package com.urchinsec.urchinflag;

import android.content.Context;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {
  Button login_button;
  
  EditText password_input;
  
  EditText username_input;
  
  protected void onCreate(Bundle paramBundle) {
    super.onCreate(paramBundle);
    setContentView(R.layout.activity_main);
    this.login_button = (Button)findViewById(R.id.login_btn);
    this.username_input = (EditText)findViewById(R.id.username_inp);
    this.password_input = (EditText)findViewById(R.id.password_inp);
    this.login_button.setOnClickListener(new View.OnClickListener() {
          final MainActivity this$0;
          
          public void onClick(View param1View) {
            if (MainActivity.this.username_input.equals("urchinsec_rang3r")) {
              if (MainActivity.this.password_input.equals("s0m334ga71344$!$")) {
                StringBuilder stringBuilder = (new StringBuilder((CharSequence)MainActivity.this.password_input)).reverse();
                String str = "urchinsec{" + MainActivity.this.username_input + "_@_" + stringBuilder + "}";
                Toast.makeText((Context)MainActivity.this, str, 1);
              } else {
                Toast.makeText((Context)MainActivity.this, "Wrong Password", 0);
              } 
            } else {
              Toast.makeText((Context)MainActivity.this, "Wrong Username", 0);
            } 
          }
        });
  }
}
