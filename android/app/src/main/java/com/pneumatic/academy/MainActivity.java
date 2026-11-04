package com.pneumatic.academy;

import android.app.*;
import android.os.Bundle;
import android.content.*;
import android.net.Uri;
import android.view.*;
import android.webkit.*;
import android.widget.*;

/** Same-origin client for the existing Python-served application. No JS/native bridge. */
public class MainActivity extends Activity {
    private WebView web;
    private String origin;
    private ValueCallback<Uri[]> fileCallback;
    private static final int PICK_FILE = 10;
    private LinearLayout root;

    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        root = new LinearLayout(this); root.setOrientation(LinearLayout.VERTICAL);
        // Target 35 enforces edge-to-edge; keep controls out of system bars and cutouts.
        root.setOnApplyWindowInsetsListener((v, insets) -> {
            v.setPadding(insets.getSystemWindowInsetLeft(), insets.getSystemWindowInsetTop(),
                insets.getSystemWindowInsetRight(), insets.getSystemWindowInsetBottom());
            return insets.consumeSystemWindowInsets();
        });
        setContentView(root);
        LinearLayout toolbar = new LinearLayout(this);
        Button settings = new Button(this); settings.setText(R.string.server_settings);
        Button reload = new Button(this); reload.setText(R.string.reload);
        toolbar.addView(settings); toolbar.addView(reload); root.addView(toolbar);
        web = new WebView(this); root.addView(web,new LinearLayout.LayoutParams(-1,0,1));
        // The existing circuit simulator needs JavaScript. Keep no native JS bridge,
        // reject off-origin navigation, and never bypass TLS errors.
        WebSettings s=web.getSettings(); s.setJavaScriptEnabled(true); s.setDomStorageEnabled(true);
        s.setAllowFileAccess(false); s.setAllowContentAccess(true);
        s.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);
        CookieManager.getInstance().setAcceptCookie(true);
        CookieManager.getInstance().setAcceptThirdPartyCookies(web,false);
        web.setWebViewClient(new WebViewClient(){
            @Override public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest req){
                return !sameOrigin(req.getUrl());
            }
            @Override public void onReceivedError(WebView view, WebResourceRequest req, WebResourceError err){
                if(req.isForMainFrame()) new AlertDialog.Builder(MainActivity.this)
                    .setTitle("Cannot reach your academy server")
                    .setMessage("Check your server address and connection. For USB testing, start Python on the laptop and run adb reverse tcp:8000 tcp:8000. Then reload.")
                    .setPositiveButton("Settings",(d,w)->configure()).setNegativeButton("Close",null).show();
            }
            // Default WebView handling rejects invalid TLS certificates.
        });
        web.setWebChromeClient(new WebChromeClient(){
            @Override public boolean onShowFileChooser(WebView v, ValueCallback<Uri[]> callback, FileChooserParams params){
                if(fileCallback!=null) fileCallback.onReceiveValue(null);
                fileCallback=callback;
                Intent intent=new Intent(Intent.ACTION_OPEN_DOCUMENT);
                intent.addCategory(Intent.CATEGORY_OPENABLE); intent.setType("text/plain");
                try { startActivityForResult(intent,PICK_FILE); }
                catch(ActivityNotFoundException e){ fileCallback.onReceiveValue(null); fileCallback=null; }
                return true;
            }
        });
        settings.setOnClickListener(v->configure()); reload.setOnClickListener(v->{if(origin!=null)web.loadUrl(origin+"/");});
        String saved=getPreferences(0).getString("server","");
        if(saved.isEmpty()) configure(); else load(saved);
    }
    private boolean sameOrigin(Uri uri){
        if(origin==null)return false;
        Uri base=Uri.parse(origin);
        return base.getScheme().equals(uri.getScheme()) && base.getHost().equals(uri.getHost()) && base.getPort()==uri.getPort();
    }
    private void configure(){
        EditText address=new EditText(this);address.setSingleLine(true);address.setInputType(17);
        address.setHint("https://academy.example.com");
        address.setText(getPreferences(0).getString("server",""));
        AlertDialog dialog=new AlertDialog.Builder(this).setTitle("Connect to your Python server")
            .setMessage("Enter an HTTPS address. A debug APK also supports http://localhost:8000 via USB forwarding. Changing servers changes the accounts/projects you see.")
            .setView(address).setPositiveButton("Connect",null).setNegativeButton("Cancel",null).create();
        dialog.setOnShowListener(d->dialog.getButton(-1).setOnClickListener(v->{
            String value=address.getText().toString().trim().replaceAll("/+$","");
            Uri u=Uri.parse(value);
            boolean debug=(getApplicationInfo().flags & android.content.pm.ApplicationInfo.FLAG_DEBUGGABLE)!=0;
            boolean local=debug && "http".equals(u.getScheme()) && ("localhost".equals(u.getHost())||"127.0.0.1".equals(u.getHost())||"10.0.2.2".equals(u.getHost()));
            if(u.getHost()==null || !("https".equals(u.getScheme())||local) || u.getUserInfo()!=null || u.getQuery()!=null || u.getFragment()!=null || (u.getPath()!=null&&!u.getPath().isEmpty())){
                address.setError("Use an HTTPS origin with no path, or debug localhost HTTP.");return;
            }
            getPreferences(0).edit().putString("server",value).apply();load(value);dialog.dismiss();
        }));dialog.show();
    }
    private void load(String value){origin=value;web.loadUrl(value+"/");}
    @Override protected void onActivityResult(int request,int result,Intent data){
        super.onActivityResult(request,result,data);
        if(request==PICK_FILE && fileCallback!=null){fileCallback.onReceiveValue(result==RESULT_OK&&data!=null&&data.getData()!=null?new Uri[]{data.getData()}:null);fileCallback=null;}
    }
    @Override public void onBackPressed(){if(web.canGoBack())web.goBack();else super.onBackPressed();}
    @Override protected void onPause(){super.onPause();web.onPause();CookieManager.getInstance().flush();}
    @Override protected void onResume(){super.onResume();if(web!=null)web.onResume();}
    @Override protected void onDestroy(){if(fileCallback!=null)fileCallback.onReceiveValue(null);web.destroy();super.onDestroy();}
}
