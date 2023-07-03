# holoEN_yolo3

本程式提供一種更加簡便的方式使用yolo3模型，原模型來自https://github.com/qqwweee/keras-yolo3

1. 簡介: 訓練模型分為三個部分，生成訓練數據、訓練模型與預測模型，本程式提供更簡便的方式完成

這三個步驟。如果你要訓練自己的模型，也可以自行提供數據和修改程式。

2. 準備訓練用數據: 使用指令

     python app.py --action data_fetch

之後，會彈出一個 UI， 要你輸入以下參數: image_path, image_path_after_record,

data_record_file。image_path 是影像存放的資料夾，image_path_after_record

是每一個影像完成紀錄後被移動到的地點， data_record_file 是用來記錄訓練集

的文字檔。輸入完參數後按下 start 後就會彈出一個影像。若想要框出一個在影像中的

物件的話，只要點一下該物件所在地方的左上角、右下角和按下所屬類別的按鈕即可。

一個影像可以框出多個物件，框完之後點擊submit，關掉影像後就能選下一個影像了。

3. 訓練模型 : 使用指令

          python app.py --action train --retrain <boolean> --annotation_path <str> --model_dir_path <str> --load_model_name <str> --save_model_name <str>--classes_path <str> --learning_rate <float> --batch_size <int> --epoch <int>

     * annotation_path 是上一步生成的文字檔
     * classes_path 是紀載所有物件類型的的文字檔，檔案格式: <class1_str>\n<class2_str>\n...<classN_str>\n
     * model_dir_path 是放置weight 的資料夾，load_model_name 是載入的weight，save_model_name
          是要輸出的weight，retrain=False 代表新生成一個weight而不是重新訓練一個權重。

     如果用自己的dataset訓練效果不理想，可以考慮修改的部分:
     1. 在 yolo3_keras\train_model_config.py 更改 optimizer 和 callback
     2. 在 yolo3_keras\yolo3\utils.py 的 get_random_data 的部分可以調整 data augmentation 的相關參數
     3. 將本程式用的 tiny model 改成 model

4. 預測結果: 使用指令

          python app.py --action  predict --weight_path <str> --class_path <str> --input_image_dir <str> --output_image_dir <str>



