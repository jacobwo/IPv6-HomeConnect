# IPv6-HomeConnect

### Inspiration & Background / 項目背景與啟發

Inspired by the **freedom.gov** project, I have decided to release my personal method for maintaining a secure and reliable connection back to Mainland China. This project has also greatly benefited from the rapid development of **AI**, which allowed for the efficient organization and finalization of these technical materials.

受 **freedom.gov** 項目的啟發，我決定發佈這套我自己長期使用的連入中國大陸的方法，以供有類似需求的人士參考。同時，本項目亦受益於近期 **AI** 的迅速發展，使我能夠快速整理本項目的技術內容。

---

### Project Overview / 項目簡介

**IPv6-HomeConnect** provides a professional solution to dynamically track and log IPv6 addresses. By leveraging a remote Linux server (with a fixed IP or DDNS) as an "Anchor," you can monitor and record the dynamic IPv6 address of a machine in Mainland China. This avoids the need for commercial DDNS services like Oray (PeanutShell) or Sunlogin, which require mandatory real-name authentication.

**IPv6-HomeConnect** 提供了一個專業的方案來動態記錄 IPv6 位址。通過利用一台境外的 Linux 主機（具備固定 IP 或 DDNS 域名）作為「錨點」（Anchor），您可以監控並記錄中國大陸境內主機的動態 IPv6 位址。這可以讓您免於使用如向日葵、花生殼等需要實名認證的 DDNS 服務。

---

### Prerequisites / 前期準備工作

#### 1. IPv6 Infrastructure in China / 中國大陸 IPv6 環境說明
Most mainstream Internet Service Providers (ISPs) in China (Telecom, Unicom, Mobile) now fully support IPv6. Based on my observations, IPv6 is available for almost all fiber-to-the-home (FTTH) connections. The only exceptions are certain community shared-broadband providers or legacy cable TV network operators. China's IPv6 deployment is very aggressive; the primary obstacle is usually the default restrictions set on the ISP-provided modems.

中國大陸主流的互聯網服務供應商（ISP，如電訊、聯通、移動）基本上都支援 IPv6。根據我的瞭解，除了部分小區的共享寬帶或傳統有線電視營運商外，絕大部分光纖接入的服務都提供了 IPv6（中國大陸的 IPv6 佈置非常激進，主要限制往往來自於光貓端的設置而非網絡基礎設施）。

#### 2. Local Infrastructure / 境內端基礎設施
A Linux host (e.g., Raspberry Pi) in China is required. You must obtain the **Admin password** for your modem (ONT). While cracking is an option, purchasing the password online (typically 5-15 RMB) is the most efficient method.

您需要一台位於中國大陸境內的 Linux 主機。您需要取得光貓的 **Admin 管理員密碼**（可以嘗試自行破解，最簡單的方法是在淘寶上購買，價格通常在 5 至 15 元人民幣）。

**Crucial Step:** Switch the modem to **Bridge Mode**. Use your own Wi-Fi Router for dialing, ensure IPv6 is enabled, and configure the router firewall to allow inbound traffic to the Linux host.

**關鍵步驟：** 使用管理員密碼將光貓更改為**「橋接模式」（Bridge Mode）**。使用您自己的 Wi-Fi 路由器進行撥號，並確保路由器已開啟 IPv6 功能，且 IPv6 防火牆已配置為支援入站訪問（Inbound）。

---

### Installation Steps / 部署步驟

#### Step 1: Deploy Anchor (Remote Side) / 第一步：部署境外端（Anchor）
On your remote server, enter the `anchor/` directory, run `make`, and **record the passwords for `sshlog` and `rdiplog`**.

首先在遠端主機進入 `anchor/` 目錄。執行 `Makefile` 並**務必記錄下 `sshlog` 與 `rdiplog` 用戶的密碼**。

```bash
cd anchor
make
sudo make install
```

#### Step 2: Configure & Deploy Beacon (Local Side) / 第二步：配置並部署境內端（Beacon）
Update `beacon/ssh_config` with your remote IP/DDNS, then run the Makefile in the `beacon/` directory.

在境內主機編輯 `beacon/ssh_config` 檔案並修改 HostName，隨後在 `beacon/` 目錄執行：

```bash
cd beacon
make                   # Setup local environment / 初始化環境
sudo make deploy_key   # Push public key / 發佈公鑰 (需輸入 sshlog 密碼)
sudo make start        # Start monitoring / 啟動監控服務
```

---

### Use Case: Financial & Government Apps / 應用實例：金融與政務 App

#### 1. Advanced Stealth for VPN Detection / 針對 VPN 檢測的高級隱匿方案
Certain apps detect if a VPN (like V2Ray) is active on the smartphone and will exit if found. It is recommended to move the VPN client to a **Home Router** or **Side-Gateway**. This allows the phone to use a Chinese IP via standard Wi-Fi without any VPN software running locally.

某些 App 會偵測手機上是否啟用了 VPN（如 V2Ray 等）；一旦偵測到，App 會直接閃退。建議將 VPN 客戶端遷移至**家用路由器**或**旁路路由器**上。這樣手機無需開啟任何 VPN 軟體即可透過 Wi-Fi 使用中國大陸 IP。

#### 2. Anti-SSID Mapping Privacy / 增強隱私建議（防 SSID 定位）
To prevent location tracking through cellular towers or Wi-Fi scanning:
為了防止透過基站或 Wi-Fi 掃描進行定位：

* **Flight Mode:** Disable cellular radios to prevent tracking via tower IDs.
* **飛行模式：** 開啟飛行模式，防止透過基站信息進行定位。
* **Bluetooth:** Disable Bluetooth to prevent tracking via nearby beacons.
* **關閉藍牙：** 關閉藍牙以防止透過周邊藍牙信標進行定位。
* **Local Network Access:** Disable "Local Network Access" for the app. This prevents the app from scanning surrounding SSID/BSSID data to pinpoint your real location via Wi-Fi mapping databases.
* **區域網絡訪問：** 在系統設置中關閉該 App 的「區域網絡訪問」權限。這能阻止 App 掃描周邊環境的 SSID/BSSID 信息，防止其透過 Wi-Fi SSID 數據庫比對出您的真實地理位置。

---

### Important Notes / 重要註解

1. **Scope:** This project only logs IPv6. For access methods like **V2Ray**, refer to their respective projects. Use ports **above 10000**.  
   **項目範圍：** 本項目僅記錄 IPv6 位址。關於 **V2Ray** 等訪問方式，請參考相關項目。建議端口設置在 **10000 以上**。
2. **Password Management:** Securely record all created passwords.  
   **密碼管理：** 請妥善記錄所有建立的密碼。

---

### Retrieval / 提取位址方法
To retrieve the latest logged IPv6 address on your remote server:  
若要在遠端伺服器上獲取最新的 IPv6 位址：

```bash
sudo -u rdiplog /home/rdiplog/rdiplog
```

---

### Author / 作者
**Jacob Wong**

### Contact / 聯繫方式
* **Email:** [github@linux.dscloud.me](mailto:github@linux.dscloud.me)
* **Note:** Feel free to open an **Issue** if you have questions or want to report your device compatibility.
* **備註：** 如有任何疑問或希望回饋設備兼容性測試結果，歡迎聯絡或提交 Issue。

### License / 授權
This project is licensed under the **MIT License**.  
本項目採用 **MIT 授權條款**。

