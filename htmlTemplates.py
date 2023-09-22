css= '''
<style>
.chat-message{
    padding:1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user{
    background-color:#2b313e
}
.chat-message.bot{
    background-color: #475063
}
.chat-message.avatar {
    width: 15%;
}
.chat-message .avatar img{
    max-width: 78px;
    max-height: 78px;
    border-radius: 50%;
    object-fit: cover;
}
.chat-message .message{
    width: 85%;
    paddings: 0 1.5rem;
    color: #fff;
    padding-left: 10px;
}

'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.ibb.co/rmZvTWh/360-F-210969565-c-IHkcr-Iz-Rp-WNZzq8ea-Qn-Yot-G4pk-Hh0-P9.jpg">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://i.ibb.co/xzfS4qP/unnamed.png">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''