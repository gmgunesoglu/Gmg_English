import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AdminComponent } from './admin.component';
import {HomeComponent} from "./home/home.component";
import {ReadingComponent} from "./reading/reading.component";
import {FormsModule} from "@angular/forms";
import {HttpClientModule} from "@angular/common/http";

const routes: Routes = [
  { path: '', component: AdminComponent, children: [
      { path: '', component: HomeComponent }, // Ana sayfa
      { path: 'reading', component: ReadingComponent },
    ] }
];

@NgModule({
  imports: [
    RouterModule.forChild(routes),
    FormsModule,
    HttpClientModule
  ],
  exports: [RouterModule]
})
export class AdminRoutingModule { }
