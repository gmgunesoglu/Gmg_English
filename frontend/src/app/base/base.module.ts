import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { BaseRoutingModule } from './base-routing.module';
import { BaseComponent } from './base.component';
import { FooterComponent } from './footer/footer.component';
import { HeaderComponent } from './header/header.component';
import { HomeComponent } from './home/home.component';
import { ReadingComponent } from './reading/reading.component';
import { UnitComponent } from './unit/unit.component';
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import { WebScoketComponent } from './web-scoket/web-scoket.component';


@NgModule({
  declarations: [
    BaseComponent,
    FooterComponent,
    HeaderComponent,
    HomeComponent,
    ReadingComponent,
    UnitComponent,
    WebScoketComponent,
  ],
  imports: [
    CommonModule,
    BaseRoutingModule,
    ReactiveFormsModule,
    FormsModule,
  ]
})
export class BaseModule { }
