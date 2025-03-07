import { Component } from '@angular/core';
import {ReadingService} from "../../services/reading.service";
import {Unit} from "../../models/unit";

@Component({
  selector: 'app-reading',
  templateUrl: './reading.component.html',
  styleUrls: ['./reading.component.scss']
})
export class ReadingComponent {

  inputText: string = ''; // Kullanıcının girdiği metin
  outputText: string = ''; // Butona basıldığında gösterilecek metin

  units: Array<Unit> = []

  constructor(
    private readingService: ReadingService
  ) {}

  ngOnInit(): void {
    this.getUnits()
  }

  getUnits(){
    this.readingService.getUnits().subscribe({
      next: (result) => {
        this.units = result
      }
    });
  }

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
