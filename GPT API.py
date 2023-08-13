import openai
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTextEdit, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QDoubleSpinBox


class ChatGPT(QMainWindow):
    def __init__(self):
        super().__init__()

        # OpenAI 인증 정보 - 수정 필요
        openai.api_key = "[API_Key 입력]"   # "" 안에 API Key 입력하셔서 사용이 가능합니다.

        self.setWindowTitle("Chat GPT")
        self.setMinimumSize(500, 700)

        self.conversation = QTextEdit()
        self.conversation.setReadOnly(True)

        self.message = QLineEdit()
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)

        self.engine_label = QLabel("Engine")
        self.engine_combobox = QComboBox()
        self.engine_combobox.addItems(["text-davinci-003","text-davinci-002", "text-curie-001", "text-babbage-001", "text-ada-001"])
        self.engine_combobox.setCurrentIndex(0)

        self.temperature_label = QLabel("Temperature")
        self.temperature_spinbox = QDoubleSpinBox()
        self.temperature_spinbox.setRange(0.0, 1.0)
        self.temperature_spinbox.setSingleStep(0.1)
        self.temperature_spinbox.setValue(0.5)

        self.top_p_label = QLabel("Top P")
        self.top_p_spinbox = QDoubleSpinBox()
        self.top_p_spinbox.setRange(0.0, 1.0)
        self.top_p_spinbox.setSingleStep(0.1)
        self.top_p_spinbox.setValue(0.9)

        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        conversation_layout = QVBoxLayout()
        conversation_layout.addWidget(self.conversation)

        message_layout = QHBoxLayout()
        message_layout.addWidget(self.message)
        message_layout.addWidget(self.send_button)

        options_layout = QHBoxLayout()
        options_layout.addWidget(self.engine_label)
        options_layout.addWidget(self.engine_combobox)
        options_layout.addWidget(self.temperature_label)
        options_layout.addWidget(self.temperature_spinbox)
        options_layout.addWidget(self.top_p_label)
        options_layout.addWidget(self.top_p_spinbox)

        layout.addLayout(conversation_layout)
        layout.addLayout(message_layout)
        layout.addLayout(options_layout)

        self.setCentralWidget(widget)

    def send_message(self):
        message = self.message.text()
        if message:
            self.conversation.append("Me: " + message)
            engine = self.engine_combobox.currentText()
            temperature = self.temperature_spinbox.value()
            top_p = self.top_p_spinbox.value()

            response = openai.Completion.create(
                model=engine,
                prompt=message,
                max_tokens=200,
                n=1,
                stop=None,
                temperature=temperature,
                top_p=top_p,
                frequency_penalty=0,
                presence_penalty=0
            )

            if response.choices[0].text:
                self.conversation.append("ChatGPT: \n================================== \n" + response.choices[0].text.strip() + "\n================================== \n")

            self.message.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ChatGPT()
    window.show()
    sys.exit(app.exec_())
