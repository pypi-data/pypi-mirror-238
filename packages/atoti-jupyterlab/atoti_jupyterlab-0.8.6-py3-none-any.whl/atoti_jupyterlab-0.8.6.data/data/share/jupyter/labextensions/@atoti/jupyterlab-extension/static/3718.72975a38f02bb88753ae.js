"use strict";(self.webpackChunk_atoti_jupyterlab_extension=self.webpackChunk_atoti_jupyterlab_extension||[]).push([[3718],{13718:(e,t,a)=>{a.d(t,{FiltersBarDateRangePicker:()=>g});var r=a(93388),n=a(81292),s=a(9617),i=a(27860),l=a.n(i),c=a(2445),o=a(12274);const d=s.DatePicker.RangePicker,g=({filter:e,onFilterChanged:t})=>{const a=(0,o.Fg)(),{startDate:s,endDate:i}=e;return(0,r.BX)("div",{css:n.css`
        display: flex;
        align-items: center;
        border: 1px solid ${a.grayScale[5]};
        border-radius: 2px;
        max-height: 28px;
      `,children:[e.isExclusionFilter&&(0,r.tZ)(c.IconExclude,{style:{marginLeft:3,marginRight:5}}),(0,r.tZ)(d,{css:n.css`
          margin: 0 4px 0 0;
        `,value:[l()(s),l()(i)],onChange:a=>{const[r,n]=a,s={...e,startDate:r.toDate(),endDate:n.toDate()};t(s)},placement:"bottomLeft",bordered:!1,allowClear:!1})]})}}}]);