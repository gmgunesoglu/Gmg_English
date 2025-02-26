import { Component, Input, Output, EventEmitter } from '@angular/core';

interface Quest {
  id: number;
  quest: string;
  option_a: string;
  option_b: string;
  option_c: string;
  option_d: string;
  correct_option: string;
  justification: string;
}

interface TextData {
  id: number;
  unit_name: string;
  title: string;
  context: string;
  quests: Quest[];
}
@Component({
  selector: 'app-text',
  templateUrl: './text.component.html',
  styleUrls: ['./text.component.scss']
})
export class TextComponent {
  @Input() text!: TextData;
  @Output() close = new EventEmitter<void>();

  closeText(): void {
    this.close.emit();
  }
}
