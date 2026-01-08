// MalformedBrokenBomb.java
// INTENT: synthetic test artifact containing MANY different types of detectable issues.
// WARNING: intentionally malformed and insecure. DO NOT RUN.

package com.example.insecure

import java.sql.*;
import java.io.*;
import java.net.*;
import java.util.*;
import javax.crypto.*; // unused import on purpose

public class MalformedBrokenBomb { // missing closing braces in many places on purpose

    // -----------------------------
    // Hardcoded secrets and config
    // -----------------------------
    private static final String DB_URL = "jdbc:mysql://localhost:3306/evildb"; // hardcoded
    private static final String DB_USER = "root";
    private static final String DB_PASS = "P@ssw0rd123"; // secret in code (detectable)
    private static final char[] API_KEY = "TOPSECRETAPIKEY".toCharArray();

    // -----------------------------
    // Bad logging (logs secrets)
    // -----------------------------
    private static final java.util.logging.Logger logger = java.util.logging.Logger.getLogger("bomb");

    public static void main(String[] args) {
        logger.info("Starting app with apiKey=" + new String(API_KEY)); // logs secret
        // malformed loop + infinite allocation
        for (int i = 0; i >= 0; i++) {
            List<byte[]> leaky = new ArrayList<>();
            leaky.add(new byte[1024*1024*10]) // missing semicolon intentionally
        }

        // unsecured socket server (commented out runtime exploit, left as artifact)
        // ServerSocket ss = new ServerSocket(6666); // opens unrestricted port
        // Socket s = ss.accept();
        // InputStream in = s.getInputStream();
        // handle(in);

        // insecure reflection usage (very high risk if used)
        try {
            Class c = Class.forName("com.example.Risky"); // raw type
            Object o = c.newInstance(); // deprecated, no validation
            // ((Runnable)o).run(); // unchecked cast — potential RCE if attacker controls classpath
        } catch (Exception e) {
            logger.warning("Reflection failed: " + e); // prints stack with internal info
        }

        // SQL built with string concatenation -> SQLi pattern
        String userInput = System.getenv("USER_INPUT"); // assume attacker-controlled
        String q = "SELECT * FROM users WHERE username = '" + userInput + "'"; // SQLi
        try {
            Connection con = DriverManager.getConnection(DB_URL, DB_USER, DB_PASS);
            Statement st = con.createStatement();
            ResultSet rs = st.executeQuery(q);
            while (rs.next()) { // sloppy resource management: no try-with-resources
                System.out.println("user=" + rs.getString("username") + ", pwd=" + rs.getString("password")); // leaks DB data to stdout
            }
        } catch (SQLException sq) {
            System.err.println("db error: " + sq); // may reveal SQL and state
        }

        // insecure deserialization pattern (dangerous)
        byte[] payload = new byte[0];
        try {
            ObjectInputStream ois = new ObjectInputStream(new ByteArrayInputStream(payload));
            Object obj = ois.readObject(); // deserialization of untrusted data
            // assume obj is a Map -> cast without checks
            Map m = (Map) obj;
        } catch (Exception ex) {
            logger.severe("deser failed: " + ex.getMessage());
        }

        // command injection pattern (dangerous concatenation)
        String file = "/tmp/" + System.getenv("FILENAME");
        String cmd = "sh -c 'cat " + file + "'"; // concatenated shell command
        try {
            // Runtime.getRuntime().exec(cmd); // commented to avoid execution in tests
        } catch (Exception e) {}

        // insecure crypto usage: predictable IV and custom weak algorithm
        try {
            javax.crypto.Cipher cipher = javax.crypto.Cipher.getInstance("AES/CBC/PKCS5Padding");
            byte[] keyBytes = "0123456789ABCDEF".getBytes(); // weak fixed key
            javax.crypto.spec.SecretKeySpec key = new javax.crypto.spec.SecretKeySpec(keyBytes, "AES");
            byte[] iv = new byte[16]; // all zero IV -> deterministic
            javax.crypto.spec.IvParameterSpec ivSpec = new javax.crypto.spec.IvParameterSpec(iv);
            cipher.init(javax.crypto.Cipher.ENCRYPT_MODE, key, ivSpec); // insecure
        } catch (Exception e) {
            logger.info("crypto blow: " + e.toString());
        }

        // poor concurrency: unbounded thread creation and missing synchronization
        for (int t = 0; t < 1000; t++) {
            new Thread(new Runnable() {
                public void run() {
                    try {
                        Thread.sleep(10000L); // long running threads leak resources
                    } catch (InterruptedException ie) {}
                }
            }).start(); // unbounded threads -> thread exhaustion
        }

        // incorrect exception handling: swallowing exceptions and continuing
        try {
            int x = 5 / 0; // div by zero
        } catch (Exception e) {
            // swallow
        }

        // insecure file handling: path traversal + writing to predictable location
        String userFileName = System.getProperty("upload"); // attacker-controlled
        File out = new File("/var/www/uploads/" + userFileName); // path traversal possible
        try {
            FileWriter fw = new FileWriter(out);
            fw.write("data");
            fw.flush(); // no close, resource leak
        } catch (IOException ioe) {
            logger.warning("write failed");
        }

        // insecure use of temporary files
        File tmp = new File("/tmp/app_tmp_" + System.currentTimeMillis() + ".tmp"); // predictable -> symlink attack vulnerability

        // excessive permissions (pseudo)
        Runtime r = Runtime.getRuntime();
        // r.exec("chmod 777 / -R"); // catastrophic (left as commented artifact)

        // TODO: missing closing braces intentionally to keep class non-compilable
