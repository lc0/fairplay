package com.brainscode.hack.fairplay;


import android.os.AsyncTask;
import android.os.Handler;
import android.support.design.widget.Snackbar;
import android.util.Log;

import java.io.BufferedReader;
import java.io.Console;
import java.io.DataOutputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;


/**
 * Created by khomenkos on 11/12/17.
 */

public class MessageTask extends AsyncTask<String, Void, String> {

    String API = "http://f4f67f16.ngrok.io/";

    ResultsListener listener;

    public void setOnResultsListener(ResultsListener listener) {
        this.listener = listener;
    }

    protected String generateMessage(String type, String values) {

        StringBuilder sb = new StringBuilder();

        String[] parts = values.split(" ");
        String payload = String.format("{\"x\":\"%s\", \"y\":\"%s\", \"z\":\"%s\"}",
                parts[0], parts[1], parts[2]);

        return String.format("%s %s", type, payload);
    }

    @Override
    protected String doInBackground(String... params) {
        Log.d("APP SEND", "ready to fire it up");
        Log.d("APP SEND", params[0]);


//        try {
//            String urlParameters = "payload=" + URLEncoder.encode(
//                    generateMessage(params[0], params[1]), "UTF-8");
//
//            executePost(this.API, urlParameters);
//
//        } catch (UnsupportedEncodingException e) {
//            e.printStackTrace();
//        }
//
        return "ok";
    }

    @Override
    protected void onPostExecute(String result) {
        Log.d("APP SEND", result);

        listener.onResultsSucceeded(result);

    }

    public static String executePost(String targetURL, String urlParameters) {
        HttpURLConnection connection = null;

        try {
            //Create connection
            URL url = new URL(targetURL);
            connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("POST");
            connection.setRequestProperty("Content-Type",
                    "application/x-www-form-urlencoded");

            connection.setRequestProperty("Content-Length",
                    Integer.toString(urlParameters.getBytes().length));
            connection.setRequestProperty("Content-Language", "en-US");

            connection.setUseCaches(false);
            connection.setDoOutput(true);

            //Send request
            DataOutputStream wr = new DataOutputStream (
                    connection.getOutputStream());
            wr.writeBytes(urlParameters);
            wr.close();

            //Get Response
            InputStream is = connection.getInputStream();
            BufferedReader rd = new BufferedReader(new InputStreamReader(is));
            StringBuilder response = new StringBuilder(); // or StringBuffer if Java version 5+
            String line;
            while ((line = rd.readLine()) != null) {
                response.append(line);
                response.append('\r');
            }
            rd.close();
            return response.toString();
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        } finally {
            if (connection != null) {
                connection.disconnect();
            }
        }
    }

}
