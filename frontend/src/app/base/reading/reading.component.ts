import { Component } from '@angular/core';

@Component({
  selector: 'app-reading',
  templateUrl: './reading.component.html',
  styleUrls: ['./reading.component.scss']
})
export class ReadingComponent {

  inputText: string = ''; // Kullanıcının girdiği metin
  outputText: string = ''; // Butona basıldığında gösterilecek metin

  updateText() {
    this.outputText = this.inputText; // Butona basıldığında input metnini output metnine aktar
  }
  getContainerHeight() {
    return this.outputText ? { 'reading-height': true } : { 'reading-full': true };
  }
  deleteText() {
    this.outputText = ""
    this.inputText = ""
  }
}
