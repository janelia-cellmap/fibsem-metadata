# Basic information about our datasets

This repository contains metadata descriptions of FIB-SEM datasets managed by the COSEM project team.

### How to view n5 or zarr data locally with neuroglancer

If you want to use neuroglancer to view data stored locally or on shared storage systems like dm11 or nrs, all you need is to run an HTTP file server from a directory containing your data with CORS enabled. An HTTP file server is a program that allows web services to access files; when you start it up, it will tell you what address + port it is running on, and you can paste that into your browser and start browsing files through your browser. CORS stands for "Cross-Origin Resource Sharing"; running an HTTP server with CORS enabled means that a website like neuroglancer can access files through your HTTP server.

1. Getting an HTTP file server running with CORS enabled.  

    There are a lot of HTTP file servers available in a lot of different languages. Personally, I use the program [`serve`](https://www.npmjs.com/package/serve), which is written in javascript and uses the NodeJS runtime. 
    
    How do you get `serve`? It is available for download via a Javascript tool called "Node Package Manager", or `npm`. `npm` allows you to install and run javascript applications. If you do not have (`npm`) installed, first install it via [these instructions](https://www.npmjs.com/get-npm).

    Alternatively, if you are using `conda` to manage software dependencies, you can install `npm` via `conda`, e.g. 

    ```
    $ conda install nodejs -c conda-forge
    ```

    Once you have `npm` installed, run the following command to install `serve`:

    ```
    $ npm install -g serve 
    ```
    (Without the `-g` part of the above command, `npm` would install `serve` to our current directory, and we would not be able to run it easily if we changed directories. `-g` tells `npm` that we want this program installed globally, so you can run `serve` no matter which directory you are in.)

    
    Once `serve` is installed, you can try it out by starting it by typing `serve` at the command line:
    
   ```bash
   $ serve
   ``` 
   If `serve` was installed correctly, you should see this:

    <pre><font color="#4E9A06">┌────────────────────────────────────────────────────┐</font>
   <font color="#4E9A06">│</font>                                                    <font color="#4E9A06">│</font>
   <font color="#4E9A06">│</font>   <font color="#4E9A06">Serving!</font>                                         <font color="#4E9A06">│</font>
   <font color="#4E9A06">│</font>                                                    <font color="#4E9A06">│</font>
   <font color="#4E9A06">│</font>   <b>- Local:</b>            http://localhost:35643       <font color="#4E9A06">│</font>
   <font color="#4E9A06">│</font>   <b>- On Your Network:</b>  http://192.168.1.154:35643   <font color="#4E9A06">│</font>
   <font color="#4E9A06">│</font>                                                    <font color="#4E9A06">│</font>
   <font color="#4E9A06">│</font>   <font color="#CC0000">This port was picked because </font><font color="#CC0000"><u style="text-decoration-style:single">5000</u></font><font color="#CC0000"> is in use.</font>     <font color="#4E9A06">│</font>
   <font color="#4E9A06">│</font>                                                    <font color="#4E9A06">│</font>
   <font color="#4E9A06">│</font>   <font color="#555753">Copied local address to clipboard!</font>               <font color="#4E9A06">│</font>
   <font color="#4E9A06">│</font>                                                    <font color="#4E9A06">│</font>
   <font color="#4E9A06">└────────────────────────────────────────────────────┘</font></pre>

   If you click on one of those URLs, your web browser should navigate to a page that shows you the files contained in the folder where you ran `serve`

   To shut down the server, press `control + c`.

   If you want to run `serve` with CORS enabled, it's very simple: just enter this at the command line:

   ```bash
   $ serve --cors
   ```
2. Viewing data from your HTTP file server with neuroglancer
    
    Once your CORS-enabled file server is running, use the web browser to navigate to a directory that contains a zarr / n5 group (for viewing multiscale data) or dataset (for viewing single resolution data). Copy your current address from the browser URL bar, then open a new tab and navigate to [neuroglancer](http://neuroglancer-demo.appspot.com/). 
    
    On the right you will see a field labelled "Data source URL". Click on that, then put `n5://` (if your data are saved as n5) or `zarr://` (if your data are saved as zarr) in front of the address to your fileserver. 
    
    
    For example, if the URL from my HTTP file server is 
    
    `http://1.150.10.225:5000/data.n5/raw/` 
    
    I would put 
    
    `n5://http://1.150.10.225:5000/data.n5/raw/` 
    
    in the "Data source URL" box. Next, hit `enter`; you should see the text "create as image layer" or "create as segmentation layer" appear on the bottom right of the window; click on this text, and view your data.